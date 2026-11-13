"""Recompute metrics from an existing predictions.jsonl (no model needed).

    python scripts/evaluate.py results/baseline_hindi_test_n200_seed42/predictions.jsonl
"""
import json
import sys
from pathlib import Path

from factindic.baseline import read_rows
from factindic.metrics import summarize_run

path = Path(sys.argv[1])
metrics = summarize_run(read_rows(path))
(path.parent / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(metrics, indent=2, ensure_ascii=False))
