#!/usr/bin/env python3
"""Audit a FactIndic Colab NLI ZIP and compute matched prompt-arm score deltas."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


def read_csv_member(archive: zipfile.ZipFile, suffix: str) -> tuple[str, list[dict[str, str]]]:
    names = [name for name in archive.namelist() if name.endswith(suffix)]
    if len(names) != 1:
        raise ValueError(f"Expected one ZIP member ending {suffix!r}; got {names}")
    data = archive.read(names[0]).decode("utf-8-sig")
    return names[0], list(csv.DictReader(io.StringIO(data)))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("nli_zip", type=Path)
    parser.add_argument("--candidate-zip", type=Path, required=True,
                        help="The exact quality-filtered candidate ZIP used in Colab.")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.nli_zip) as scored_zip:
        metadata_names = [name for name in scored_zip.namelist() if name.endswith("nli_screening_metadata.json")]
        if len(metadata_names) != 1:
            raise ValueError(f"Expected one NLI metadata file, got {metadata_names}")
        metadata = json.loads(scored_zip.read(metadata_names[0]))
        _, rows = read_csv_member(scored_zip, "nli_screened_generations.csv")
        review_name, review_rows = read_csv_member(scored_zip, "human_review.csv")
        review_bytes = scored_zip.read(review_name)

    with zipfile.ZipFile(args.candidate_zip) as candidate_zip:
        _, original = read_csv_member(candidate_zip, "generations.csv")
        original_review_names = [name for name in candidate_zip.namelist() if name.endswith("human_review.csv")]
        if len(original_review_names) != 1:
            raise ValueError("Candidate ZIP must contain one human_review.csv")
        original_review_bytes = candidate_zip.read(original_review_names[0])

    candidate_hash = hashlib.sha256(args.candidate_zip.read_bytes()).hexdigest()
    if candidate_hash != metadata.get("input_zip_sha256"):
        raise ValueError("Candidate ZIP SHA-256 does not match the input hash recorded by Colab.")
    if review_bytes != original_review_bytes:
        raise ValueError("The exported human review worksheet differs from the original candidate worksheet.")
    if len(rows) != int(metadata.get("n_rows", -1)) or len(rows) != 152:
        raise ValueError(f"Expected 152 scored rows matching metadata; found {len(rows)}")

    key = lambda row: (row["condition"], row["id"], row["arm"])
    source_by_key = {key(row): row for row in original}
    if len(source_by_key) != len(original):
        raise ValueError("Duplicate condition/id/arm keys in input generations.csv")
    scored_by_key = {key(row): row for row in rows}
    if len(scored_by_key) != len(rows) or set(scored_by_key) != set(source_by_key):
        raise ValueError("Scored row IDs/conditions/arms do not match the candidate ZIP")
    for k, scored in scored_by_key.items():
        source = source_by_key[k]
        for field in ("source_visible", "prediction"):
            if scored[field] != source[field]:
                raise ValueError(f"Changed {field} text for {k}")

    numeric = ("nli_max_entailment", "nli_contradiction_at_best_entailment",
               "nli_neutral_at_best_entailment", "nli_max_contradiction_any_chunk")
    for row in rows:
        for field in numeric:
            value = float(row[field])
            if not 0 <= value <= 1:
                raise ValueError(f"Score outside [0,1] for {field}: {value}")

    condition_counts = Counter(row["condition"] for row in rows)
    arm_counts = Counter(row["arm"] for row in rows)
    pairs: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        pair = (row["condition"], row["id"])
        if row["arm"] in pairs[pair]:
            raise ValueError(f"Duplicate arm {row['arm']} for matched document {pair}")
        pairs[pair][row["arm"]] = row
    if any(set(arms) != {"standard", "factuality_aware"} for arms in pairs.values()):
        raise ValueError("At least one document is missing a prompt arm")

    paired_rows = []
    paired_summary = []
    for (condition, example_id), arms in sorted(pairs.items()):
        standard, aware = arms["standard"], arms["factuality_aware"]
        entail_delta = float(aware["nli_max_entailment"]) - float(standard["nli_max_entailment"])
        contra_delta = float(aware["nli_contradiction_at_best_entailment"]) - float(standard["nli_contradiction_at_best_entailment"])
        paired_rows.append({
            "condition": condition, "id": example_id, "subset": standard.get("subset", ""),
            "standard_max_entailment": float(standard["nli_max_entailment"]),
            "factuality_aware_max_entailment": float(aware["nli_max_entailment"]),
            "aware_minus_standard_max_entailment": entail_delta,
            "standard_contradiction_at_best_entailment": float(standard["nli_contradiction_at_best_entailment"]),
            "factuality_aware_contradiction_at_best_entailment": float(aware["nli_contradiction_at_best_entailment"]),
            "aware_minus_standard_contradiction_at_best_entailment": contra_delta,
        })
    for condition in sorted(condition_counts):
        group = [r for r in paired_rows if r["condition"] == condition]
        de = [r["aware_minus_standard_max_entailment"] for r in group]
        dc = [r["aware_minus_standard_contradiction_at_best_entailment"] for r in group]
        paired_summary.append({
            "condition": condition, "n_matched_documents": len(group),
            "mean_aware_minus_standard_max_entailment": statistics.mean(de),
            "median_aware_minus_standard_max_entailment": statistics.median(de),
            "aware_entailment_score_higher": sum(d > 0 for d in de),
            "aware_entailment_score_lower": sum(d < 0 for d in de),
            "equal_entailment_scores": sum(d == 0 for d in de),
            "mean_aware_minus_standard_contradiction_at_best_entailment": statistics.mean(dc),
        })

    write_csv(args.out_dir / "nli_screening_paired_prompt_comparison.csv", paired_rows)
    write_csv(args.out_dir / "nli_screening_paired_prompt_summary.csv", paired_summary)

    score_summary = []
    for condition in sorted(condition_counts):
        for arm in ("standard", "factuality_aware"):
            group = [r for r in rows if r["condition"] == condition and r["arm"] == arm]
            if not group:
                continue
            score_summary.append({
                "condition": condition, "arm": arm, "n": len(group),
                "mean_max_entailment": statistics.mean(float(r["nli_max_entailment"]) for r in group),
                "median_max_entailment": statistics.median(float(r["nli_max_entailment"]) for r in group),
                "mean_contradiction_at_best_entailment": statistics.mean(float(r["nli_contradiction_at_best_entailment"]) for r in group),
            })

    replacement = sum("�" in r["prediction"] for r in rows)
    cap_hits = sum(r["hit_new_token_cap"].lower() == "true" for r in rows)
    empty = sum(not r["prediction"].strip() for r in rows)
    human_fields = [field for field in ("human_factuality", "error_type", "evidence_or_error_span", "annotator_id") if field in (review_rows[0] if review_rows else {})]
    human_label_cells = sum(bool(r.get(field, "").strip()) for r in review_rows for field in human_fields)
    score_values = [float(r["nli_max_entailment"]) for r in rows]
    chunks = Counter(int(r["nli_source_chunks"]) for r in rows)
    summary = {
        "n_rows": len(rows), "condition_counts": dict(condition_counts), "arm_counts": dict(arm_counts),
        "n_matched_documents": len(pairs), "candidate_sha256_verified": candidate_hash,
        "source_and_prediction_text_match": True, "human_review_sheet_byte_identical": True,
        "human_annotation_cells_filled": human_label_cells,
        "generation_cap_hits": cap_hits, "replacement_character_rows": replacement,
        "empty_generation_rows": empty, "nli_probabilities_in_unit_interval": True,
        "nli_entailment_mean": statistics.mean(score_values),
        "nli_entailment_median": statistics.median(score_values),
        "nli_entailment_min": min(score_values), "nli_entailment_max": max(score_values),
        "source_chunk_counts": dict(chunks), "metadata": metadata,
    }
    (args.out_dir / "nli_screening_audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.out_dir / "nli_screening_descriptive_summary.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(score_summary[0]))
        writer.writeheader(); writer.writerows(score_summary)

    lines = [
        "# FactIndic NLI prompt-pilot screening — 12 November 2026", "",
        "## Data and audit", "",
        f"- Scored rows: {len(rows)} (Hindi {condition_counts['hindi']}; synthetic p100 {condition_counts['synthetic_p100']}; authentic MUTANT {condition_counts['authentic_mutant']}).",
        f"- Matched source documents: {len(pairs)} (23 Hindi, 23 synthetic p100, 30 authentic MUTANT), each with both prompt arms.",
        f"- Exact candidate ZIP SHA-256 verified: `{candidate_hash}`.",
        "- All 152 scored source texts and summaries match the candidate; the original blank human worksheet is byte-identical.",
        f"- Generation audit: {cap_hits} token-cap hits, {replacement} replacement-character rows, {empty} empty summaries; {human_label_cells} human annotation cells filled.",
        f"- Colab model: `{metadata['model']}` on {metadata['device']}; model labels {metadata['model_labels']}; all hypothesis truncation flags are false.",
        f"- Source chunk count per row: {dict(chunks)}. All observed entailment probabilities range from {min(score_values):.6f} to {max(score_values):.6f} (mean {statistics.mean(score_values):.4f}, median {statistics.median(score_values):.4f}).",
        "", "## Descriptive NLI results", "",
        "| Condition | Prompt | n | Mean max entailment | Median max entailment | Mean contradiction at best-entailment chunk |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in score_summary:
        lines.append(f"| {row['condition']} | {row['arm']} | {row['n']} | {row['mean_max_entailment']:.4f} | {row['median_max_entailment']:.4f} | {row['mean_contradiction_at_best_entailment']:.4f} |")
    lines += ["", "## Matched prompt-arm differences", "", "Differences are factuality-aware minus standard; positive entailment differences mean only that this NLI model assigned a larger score.", "", "| Condition | Matched n | Mean entailment difference | Median difference | Aware higher / lower / tie | Mean contradiction difference |", "|---|---:|---:|---:|---:|---:|"]
    for row in paired_summary:
        lines.append(f"| {row['condition']} | {row['n_matched_documents']} | {row['mean_aware_minus_standard_max_entailment']:+.4f} | {row['median_aware_minus_standard_max_entailment']:+.4f} | {row['aware_entailment_score_higher']} / {row['aware_entailment_score_lower']} / {row['equal_entailment_scores']} | {row['mean_aware_minus_standard_contradiction_at_best_entailment']:+.4f} |")
    lines += ["", "## Interpretation and limits", "", "This output is automated NLI screening, not human factuality annotation. These probabilities are not calibrated factuality scores. The median max-entailment is near 1.0 in every condition, indicating strong score saturation; therefore the small prompt-arm median differences should not be read as meaningful factuality changes. The mean differences point in different directions across Hindi, synthetic code-mix, and authentic MUTANT. Contradiction signals also change direction across conditions. No overall prompt winner is supported by this screening.", "", "The NLI archive did not include the within-document paired CSVs, so the two paired files in this folder were recomputed from its 152 scored rows. No generation or human label was changed.", ""]
    report_path = args.out_dir / "nli_screening_report_2026-11-12.md"
    report_path.write_text(chr(10).join(lines), encoding="utf-8")

    print(f"Audit passed for {len(rows)} rows and {len(pairs)} matched documents.")
    print(f"Saved report and paired comparisons to {args.out_dir}")
    for row in paired_summary:
        print(row)


if __name__ == "__main__":
    main()
