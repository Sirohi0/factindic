#!/usr/bin/env python3
"""Summarize assistant-only source-check labels for the FactIndic pilot.

This script does not infer factuality. It aggregates the assistant review labels
already recorded in the input CSV and reports paired label movement descriptively.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

LABELS = ("supported", "minor_error", "major_error", "unverifiable")
SEVERITY = {label: index for index, label in enumerate(LABELS)}
CONDITIONS = ("hindi", "synthetic_p100", "authentic_mutant")
ARMS = ("standard", "factuality_aware")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No rows found in {path}")
    required = {"condition", "id", "arm", "assistant_preliminary_label"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return rows


def summarize(rows: list[dict[str, str]]) -> tuple[list[str], dict[str, dict[str, int]]]:
    seen: set[tuple[str, str, str]] = set()
    grouped: dict[str, dict[str, dict[str, str]]] = {c: {a: {} for a in ARMS} for c in CONDITIONS}
    for row in rows:
        condition, arm = row["condition"], row["arm"]
        label = row["assistant_preliminary_label"]
        if condition not in grouped or arm not in ARMS:
            raise ValueError(f"Unexpected condition/arm: {condition!r}/{arm!r}")
        if label not in LABELS:
            raise ValueError(f"Unexpected assistant label: {label!r}")
        key = (condition, row["id"], arm)
        if key in seen:
            raise ValueError(f"Duplicate condition/id/arm row: {key}")
        seen.add(key)
        grouped[condition][arm][row["id"]] = label

    report = [
        "# Assistant-only prompt comparison",
        "",
        "This is a descriptive aggregation of preliminary assistant source-check labels. It is not human-verified factuality data, a calibrated factuality score, or evidence that a prompt is more factually accurate. The assistant review was not blinded to prompt arm.",
        "",
        "Seven paired Hindi/synthetic-p100 article IDs were excluded symmetrically after generation-quality checks; the retained sample has 23 paired IDs and 30 authentic MUTANT examples.",
        "",
        "| Condition | n per arm | Standard labeled supported | Factuality-aware labeled supported | Difference |",
        "|---|---:|---:|---:|---:|",
    ]
    details: dict[str, dict[str, int]] = {}
    total_std = total_aware = total_n = total_better = total_worse = total_same = 0
    for condition in CONDITIONS:
        std = grouped[condition]["standard"]
        aware = grouped[condition]["factuality_aware"]
        if set(std) != set(aware):
            raise ValueError(f"Prompt arms have unmatched IDs in {condition}")
        n = len(std)
        if n == 0:
            raise ValueError(f"No examples found for {condition}")
        std_supported = sum(label == "supported" for label in std.values())
        aware_supported = sum(label == "supported" for label in aware.values())
        better = worse = same = 0
        for article_id in std:
            s_rank = SEVERITY[std[article_id]]
            a_rank = SEVERITY[aware[article_id]]
            if a_rank < s_rank:
                better += 1
            elif a_rank > s_rank:
                worse += 1
            else:
                same += 1
        delta = aware_supported - std_supported
        pp = 100 * delta / n
        report.append(
            f"| {condition.replace('_', ' ').title()} | {n} | {std_supported} ({100*std_supported/n:.1f}%) | {aware_supported} ({100*aware_supported/n:.1f}%) | {delta:+d} ({pp:+.1f} points) |"
        )
        details[condition] = {"n": n, "standard_supported": std_supported, "aware_supported": aware_supported,
                              "better": better, "worse": worse, "same": same}
        total_std += std_supported
        total_aware += aware_supported
        total_n += n
        total_better += better
        total_worse += worse
        total_same += same

    report.extend([
        f"| **All conditions** | **{total_n}** | **{total_std} ({100*total_std/total_n:.1f}%)** | **{total_aware} ({100*total_aware/total_n:.1f}%)** | **{total_aware-total_std:+d} ({100*(total_aware-total_std)/total_n:+.1f} points)** |",
        "",
        "## Paired label movement",
        "",
        "Severity order for this descriptive tally: supported < minor_error < major_error < unverifiable.",
        "",
        "| Condition | Aware arm improved | Aware arm worsened | Same label |",
        "|---|---:|---:|---:|",
    ])
    for condition in CONDITIONS:
        d = details[condition]
        report.append(f"| {condition.replace('_', ' ').title()} (n={d['n']}) | {d['better']} | {d['worse']} | {d['same']} |")
    report.extend([
        f"| **All (n={total_n})** | **{total_better}** | **{total_worse}** | **{total_same}** |",
        "",
        "## Limitations",
        "",
        "- These values count assistant screening labels only. Do not call them factuality accuracy or human factuality results.",
        "- The assistant saw the prompt-arm labels while reviewing, so judgments were not blinded.",
        "- The sample is small, quality-filtered, and excludes seven paired IDs with generation failures.",
        "- Human worksheet fields remain blank; this script does not fill or replace them.",
        "",
    ])
    return report, details


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=Path("results/prompt_pilot_review_candidate_2026-11-09/assistant_verification_all_152.csv"))
    parser.add_argument("--output", type=Path, default=Path("results/assistant_only_prompt_comparison_2026-11-09.md"))
    args = parser.parse_args()
    report, _ = summarize(read_rows(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote assistant-only descriptive summary: {args.output}")


if __name__ == "__main__":
    main()
