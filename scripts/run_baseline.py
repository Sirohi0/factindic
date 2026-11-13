"""Run the baseline on a reproducible sample and write predictions + metrics.

Examples:
    python scripts/run_baseline.py --dry-run                 # no download, no model: checks the pipeline
    python scripts/run_baseline.py --n 50                    # small first run
    python scripts/run_baseline.py --n 500 --device cpu
Re-running the same command resumes where it stopped.
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from factindic.baseline import MT5Summarizer, read_rows, run_baseline
from factindic.config import DEFAULT
from factindic.data import load_split
from factindic.metrics import summarize_run
from factindic.repro import collect_run_meta


def dry_run_frame() -> pd.DataFrame:
    return pd.DataFrame({
        "id": ["d1", "d2", "d3"],
        "url": ["", "", ""],
        "title": ["", "", ""],
        "summary": ["भारत में प्रदूषण बढ़ रहा है", "सरकार ने नई योजना शुरू की", "टीम ने मैच 3 रन से जीता"],
        "text": [
            "भारत में प्रदूषण का स्तर लगातार बढ़ रहा है। विशेषज्ञों के अनुसार यह चिंता का विषय है।",
            "सरकार ने किसानों के लिए नई योजना शुरू की है। इसमें 2000 रुपये दिए जाएंगे।",
            "रविवार को हुए मैच में टीम ने 3 रन से जीत दर्ज की। कप्तान ने 120 रन बनाए।",
        ],
    })


def dry_run_summarizer(texts):
    return [{"prediction": " ".join(t.split()[:6]), "input_tokens": len(t.split()), "truncated": False}
            for t in texts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200, help="documents to sample (default 200)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--device", default="auto", help="auto, cpu, mps or cuda")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--dry-run", action="store_true", help="3 built-in documents and a fake summarizer")
    ap.add_argument("--data-jsonl", default=None,
                    help="run on a prepared dataset (columns id, text, summary), e.g. from make_codemixed.py")
    args = ap.parse_args()

    cfg = DEFAULT
    if args.dry_run:
        df, n, summarizer, device = dry_run_frame(), None, dry_run_summarizer, "none"
        name = "dry_run"
        if args.data_jsonl:
            df = pd.read_json(args.data_jsonl, lines=True, dtype={"id": str})
            df["id"] = df["id"].astype(str)
            name = "dry_run_" + Path(args.data_jsonl).stem
    else:
        if args.data_jsonl:
            df = pd.read_json(args.data_jsonl, lines=True, dtype={"id": str})
            df["id"] = df["id"].astype(str)
            n, name = None, "baseline_" + Path(args.data_jsonl).stem
        else:
            df, n = load_split(cfg, n=args.n, seed=args.seed), args.n
            name = f"baseline_{cfg.language}_{cfg.split}_n{args.n}_seed{args.seed}"
        summarizer = MT5Summarizer(cfg, device=args.device)
        device = summarizer.device
        summarizer(["यह एक छोटा परीक्षण वाक्य है।"])  # warm-up, not timed or saved

    out_dir = Path(args.out_dir or f"results/{name}")
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = collect_run_meta(cfg, n=n, seed=args.seed, batch_size=args.batch_size, device=device,
                            sample_ids=df["id"].tolist(), dry_run=args.dry_run)
    (out_dir / "run_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    pred_path = out_dir / "predictions.jsonl"
    run_baseline(summarizer, df, pred_path, batch_size=args.batch_size)

    wanted = set(df["id"].astype(str))
    rows = [r for r in read_rows(pred_path) if r["id"] in wanted]
    metrics = summarize_run(rows)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_dir}/ (run_meta.json, metrics.json, predictions.jsonl)")


if __name__ == "__main__":
    main()
