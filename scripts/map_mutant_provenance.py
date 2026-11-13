#!/usr/bin/env python3
"""Map local MUTANT sample text to files in a pinned official HF revision."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

DATASET_ID = "LingoIITGN/MUTANT"
DEFAULT_REVISION = "e7a454a71d4f9d1f3ebb65544868610e513d9366"
SUBSETS = {"PM-speech": "pm-speech", "Mankibaat": "mankibaat"}
API_ROOT = f"https://huggingface.co/api/datasets/{DATASET_ID}"
HF_ROOT = f"https://huggingface.co/datasets/{DATASET_ID}"


def get_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "FactIndic-provenance-audit/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def get_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "FactIndic-provenance-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\ufeff", "")
    return re.sub(r"\s+", " ", text).strip()


def list_files(revision: str) -> list[tuple[str, str]]:
    result = []
    for subset, folder in SUBSETS.items():
        url = f"{API_ROOT}/tree/{revision}/{folder}?recursive=true"
        for item in get_json(url):
            if item.get("type") == "file" and item.get("path", "").endswith(".txt"):
                result.append((subset, item["path"]))
    return result


def read_upstream(item: tuple[str, str], revision: str):
    subset, path = item
    url = f"{HF_ROOT}/resolve/{revision}/{path}"
    return subset, path, normalize(get_text(url))


def classify(target: str, files: list[tuple[str, str]]) -> tuple[str, list[str]]:
    exact = [path for path, text in files if target == text]
    if exact:
        return ("exact" if len(exact) == 1 else "ambiguous_exact"), exact

    prefix = [path for path, text in files if len(target) < len(text) and text.startswith(target)]
    if prefix:
        return ("exact_prefix" if len(prefix) == 1 else "ambiguous_exact_prefix"), prefix

    spans = [path for path, text in files if len(target) >= 200 and target in text]
    if spans:
        return ("unique_exact_span" if len(spans) == 1 else "ambiguous_exact_span"), spans
    return "unmatched", []


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=project_root / "authentic_code_mixed_candidates.csv")
    parser.add_argument("--output", type=Path, default=project_root / "results/mutant_source_provenance_map_2026-11-13.csv")
    parser.add_argument("--pilot-metadata", type=Path, default=project_root / "results/prompt_pilot_review_candidate_2026-11-09/run_metadata.json")
    parser.add_argument("--revision", default=DEFAULT_REVISION, help="Pinned Hugging Face dataset commit SHA")
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    selected_authentic_ids = None
    if args.pilot_metadata.exists():
        with args.pilot_metadata.open(encoding="utf-8") as handle:
            selected_authentic_ids = {str(value) for value in json.load(handle).get("selected_authentic_ids", [])}
    required = {"id", "subset", "text"}
    if candidates and not required.issubset(candidates[0]):
        raise ValueError(f"Input is missing columns: {sorted(required - set(candidates[0]))}")
    if any(row["subset"] not in SUBSETS for row in candidates):
        invalid = sorted({row["subset"] for row in candidates if row["subset"] not in SUBSETS})
        raise ValueError(f"Unknown subset labels: {invalid}")

    items = list_files(args.revision)
    upstream: dict[str, list[tuple[str, str]]] = {subset: [] for subset in SUBSETS}
    errors = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(read_upstream, item, args.revision) for item in items]
        for future in as_completed(futures):
            try:
                subset, path, text = future.result()
                upstream[subset].append((path, text))
            except Exception as exc:  # preserve full-run diagnostics, fail if any source file is unavailable
                errors.append(str(exc))
    if errors:
        raise RuntimeError(f"Could not retrieve {len(errors)} upstream files; first errors: {errors[:3]}")

    fields = [
        "local_sample_id", "declared_subset", "mapping_status", "text_match_type",
        "upstream_file_path_or_candidates", "dataset_file_url_or_candidates",
        "local_text_sha256", "prompt_pilot_included", "match_rule", "dataset_id", "dataset_revision",
    ]
    out_rows = []
    for row in candidates:
        match_type, paths = classify(normalize(row["text"]), upstream[row["subset"]])
        urls = [f"{HF_ROOT}/blob/{args.revision}/{path}" for path in paths]
        out_rows.append({
            "local_sample_id": row["id"],
            "declared_subset": row["subset"],
            "mapping_status": "ambiguous" if match_type.startswith("ambiguous") else ("unmatched" if not paths else "unique_file_match"),
            "text_match_type": match_type,
            "upstream_file_path_or_candidates": " | ".join(paths),
            "dataset_file_url_or_candidates": " | ".join(urls),
            "local_text_sha256": hashlib.sha256(row["text"].encode("utf-8")).hexdigest(),
            "prompt_pilot_included": "not_available" if selected_authentic_ids is None else ("yes" if row["id"] in selected_authentic_ids else "no"),
            "match_rule": "Exact text after Unicode NFC normalization and whitespace collapse; full-file equality, prefix, or in-file span as classified.",
            "dataset_id": DATASET_ID,
            "dataset_revision": args.revision,
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    counts = {}
    for row in out_rows:
        counts[row["mapping_status"]] = counts.get(row["mapping_status"], 0) + 1
    pilot_rows = [row for row in out_rows if row["prompt_pilot_included"] == "yes"]
    pilot_ambiguous = sum(row["mapping_status"] == "ambiguous" for row in pilot_rows)
    print(f"Revision: {args.revision}")
    print(f"Upstream text files checked: {len(items)}")
    print(f"Local candidate rows: {len(out_rows)}")
    print(f"Mapping counts: {counts}")
    if selected_authentic_ids is not None:
        print(f"Prompt-pilot authentic rows: {len(pilot_rows)}; ambiguous: {pilot_ambiguous}")
    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, urllib.error.URLError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
