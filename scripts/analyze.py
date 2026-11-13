"""Phase 2 failure analysis on a finished baseline run.

    python scripts/analyze.py results/baseline_hindi_test_n500_seed42/predictions.jsonl

Writes next to the predictions file:
    analysis.json       aggregate rates, overall and split by truncated / not truncated
    flags.jsonl         per-document check results (reused by the Phase 3 verifier)
    review_sample.csv   flagged cases plus controls, with empty error_type/notes columns to fill by hand
"""
import argparse
import csv
import json
from pathlib import Path

from factindic.analysis import analyze_rows, review_sample
from factindic.baseline import read_rows

ap = argparse.ArgumentParser()
ap.add_argument("predictions")
ap.add_argument("--flagged", type=int, default=30, help="flagged documents to put in the review sheet")
ap.add_argument("--controls", type=int, default=10, help="unflagged documents to put in the review sheet")
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--source-key", default="text",
                help='column used as the source for the checks; use "source_hi" for code-mixed runs')
ap.add_argument("--suffix", default="", help="optional filename suffix, e.g. _source_hi, to keep analyses separate")
args = ap.parse_args()

path = Path(args.predictions)
rows = read_rows(path)
analysis, checks = analyze_rows(rows, args.source_key)
suffix = args.suffix

(path.parent / f"analysis{suffix}.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
with open(path.parent / f"flags{suffix}.jsonl", "w", encoding="utf-8") as f:
    for c in checks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

sample = review_sample(rows, checks, args.flagged, args.controls, args.seed, source_key=args.source_key)
sample_fields = ["id", "truncated", "auto_flags", "reference", "prediction", "source_start", "error_type", "notes"]
with open(path.parent / f"review_sample{suffix}.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=sample_fields)
    w.writeheader()
    w.writerows(sample)

o = analysis["overall"]
print(json.dumps(o, indent=2, ensure_ascii=False))
for name, sub in analysis["by_truncation"].items():
    print(f"\n{name}: n={sub['n_documents']}, docs_flagged={sub['docs_flagged']}, "
          f"mean_novel_rate={sub['mean_novel_rate']}, ROUGE-1 F1={sub['metrics']['rouge']['rouge1']['fmeasure']}")
print(f"\nWrote analysis{suffix}.json, flags{suffix}.jsonl and review_sample{suffix}.csv ({len(sample)} rows) to {path.parent}/")
