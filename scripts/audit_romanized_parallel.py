#!/usr/bin/env python3
"""Audit aligned line-based Romanized Hinglish source/reference files.

This checks file alignment and script characteristics. Latin-script counts do
not establish that a source is genuinely code-mixed; inspect the private sample
sheet before treating the corpus as valid Hinglish.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

DEVANAGARI = re.compile(r"[\u0900-\u097F]")
LATIN = re.compile(r"[A-Za-z]")


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="GupShup h2e .source file")
    parser.add_argument("--target", required=True, type=Path, help="Aligned English .target file")
    parser.add_argument("--output", required=True, type=Path, help="Private/local output directory")
    parser.add_argument("--sample-size", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.sample_size < 1:
        parser.error("--sample-size must be at least 1")
    for path in (args.source, args.target):
        if not path.is_file():
            parser.error(f"file not found: {path}")

    sources = read_lines(args.source)
    targets = read_lines(args.target)
    if len(sources) != len(targets):
        raise SystemExit(
            f"Alignment failure: {len(sources)} source lines but {len(targets)} target lines."
        )
    if not sources:
        raise SystemExit("No aligned rows found.")

    rows = []
    for index, (source, target) in enumerate(zip(sources, targets), start=1):
        latin = len(LATIN.findall(source))
        devanagari = len(DEVANAGARI.findall(source))
        rows.append({
            "row_id": f"line_{index:06d}",
            "source": source,
            "reference": target,
            "source_chars": len(source),
            "source_words_whitespace": len(source.split()),
            "source_latin_letters": latin,
            "source_devanagari_chars": devanagari,
            "source_has_latin": latin > 0,
            "source_has_devanagari": devanagari > 0,
            "source_is_blank": not source.strip(),
            "reference_is_blank": not target.strip(),
        })

    latin_counts = [row["source_latin_letters"] for row in rows]
    dev_counts = [row["source_devanagari_chars"] for row in rows]
    nonblank_sources = [row for row in rows if not row["source_is_blank"]]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    sample = rng.sample(rows, min(args.sample_size, len(rows)))
    sample_path = output / "private_script_review_sample.csv"
    with sample_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(sample[0]))
        writer.writeheader()
        writer.writerows(sample)

    summary = {
        "task": "GupShup h2e Romanized Hindi-English to English summary",
        "rows": len(rows),
        "source_file": args.source.name,
        "target_file": args.target.name,
        "source_sha256": sha256(args.source),
        "target_sha256": sha256(args.target),
        "source_blank_rows": sum(row["source_is_blank"] for row in rows),
        "reference_blank_rows": sum(row["reference_is_blank"] for row in rows),
        "source_rows_with_latin": sum(row["source_has_latin"] for row in rows),
        "source_rows_with_devanagari": sum(row["source_has_devanagari"] for row in rows),
        "mean_source_latin_letters": round(statistics.mean(latin_counts), 2),
        "mean_source_devanagari_chars": round(statistics.mean(dev_counts), 2),
        "sample_size": len(sample),
        "sample_seed": args.seed,
        "script_counts_are_not_human_hinglish_validation": True,
        "review_sample_path": sample_path.name,
        "do_not_publish_dataset_or_sample_rows": True,
        "warning": "Review the private sample for actual Hindi-English mixing, source quality, and target alignment before modeling.",
    }
    (output / "audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Aligned rows: {len(rows)}")
    print(f"Blank source/reference rows: {summary['source_blank_rows']}/{summary['reference_blank_rows']}")
    print(f"Sources containing Latin letters: {summary['source_rows_with_latin']}/{len(rows)}")
    print(f"Sources containing Devanagari: {summary['source_rows_with_devanagari']}/{len(rows)}")
    print(f"Private review sample: {sample_path}")
    print("Script counts do not prove that the sources are genuinely Hinglish; inspect the sample.")


if __name__ == "__main__":
    main()
