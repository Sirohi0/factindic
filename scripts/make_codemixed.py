"""Build code-mixed versions of the documents in a finished Hindi baseline run.

    python scripts/make_codemixed.py results/baseline_hindi_test_n500_seed42/predictions.jsonl --p 0.5 1.0

Writes data/codemixed_<run>_p<level>.jsonl (columns: id, text, summary, source_hi, reference_hi, cmi_*).
The same 500 documents are used, so Hindi and code-mixed results are directly comparable.
Facts cannot change: only whole lexicon words are swapped; numbers, dates and names are untouched.
"""
import argparse
import json
from pathlib import Path
from statistics import mean, median

from factindic.baseline import read_rows
from factindic.codemix import make_pair
from factindic.lexicon_hi_en import LEXICON

ap = argparse.ArgumentParser()
ap.add_argument("predictions")
ap.add_argument("--p", type=float, nargs="+", default=[0.5, 1.0], help="substitution probability per lexicon word")
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--out-dir", default="data")
args = ap.parse_args()

src = Path(args.predictions)
rows = read_rows(src)
out_dir = Path(args.out_dir)
out_dir.mkdir(parents=True, exist_ok=True)
stem = src.parent.name.replace("baseline_", "")
print(f"{len(rows)} documents, lexicon of {len(LEXICON)} words\n")

for p in args.p:
    pairs = [make_pair(r["id"], r["text"], r["reference"], p, args.seed) for r in rows]
    path = out_dir / f"codemixed_{stem}_p{int(round(p * 100)):03d}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for d in pairs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    c = [d["cmi_text"] for d in pairs]
    print(f"p={p}: wrote {path}")
    print(f"   CMI of articles: mean {mean(c):.1f}, median {median(c):.1f}, max {max(c):.1f}; "
          f"substitutions per article: {mean(d['n_substitutions'] for d in pairs):.1f}; "
          f"CMI of reference summaries: mean {mean(d['cmi_summary'] for d in pairs):.1f}")
print("\nRead a few rows by eye before using the data. CMI of 0 means purely monolingual.")
