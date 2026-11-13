"""Aggregate the checks over a run and pick cases for manual error labelling."""
from __future__ import annotations

import random

from .checks import check_summary, extract_numbers
from .metrics import summarize_run

NOVEL_RATE_FLAG = 0.3  # share of summary words absent from the source


def is_flagged(c: dict) -> bool:
    return bool(c["unsupported_numbers"] or c["unsupported_dates"] or c["novel_rate"] >= NOVEL_RATE_FLAG)


def check_rows(rows: list[dict], source_key: str = "text") -> list[dict]:
    """source_key="source_hi" checks a code-mixed run against the original Hindi article,
    which isolates summary errors from the effect of swapped words."""
    return [{"id": r["id"], **check_summary(r.get(source_key, r["text"]), r["prediction"])} for r in rows]


def _support_stats(rows: list[dict], checks: list[dict]) -> dict:
    pred_total = sum(len(c["numbers"]) for c in checks)
    pred_unsup = sum(len(c["unsupported_numbers"]) for c in checks)
    ref_total = ref_kept = 0
    for r in rows:
        pred_set = set(extract_numbers(r["prediction"]))
        ref_nums = extract_numbers(r["reference"])
        ref_total += len(ref_nums)
        ref_kept += sum(n in pred_set for n in ref_nums)
    n = max(len(rows), 1)
    return {
        "n_documents": len(rows),
        "summaries_with_numbers": sum(bool(c["numbers"]) for c in checks),
        "number_support_rate": round(1 - pred_unsup / pred_total, 4) if pred_total else None,
        "docs_with_unsupported_number": sum(bool(c["unsupported_numbers"]) for c in checks),
        "reference_numbers_total": ref_total,
        "number_preservation_rate": round(ref_kept / ref_total, 4) if ref_total else None,
        "summaries_with_dates": sum(bool(c["dates"]) for c in checks),
        "docs_with_unsupported_date": sum(bool(c["unsupported_dates"]) for c in checks),
        "mean_novel_rate": round(sum(c["novel_rate"] for c in checks) / n, 4),
        "docs_flagged": sum(is_flagged(c) for c in checks),
    }


def analyze_rows(rows: list[dict], source_key: str = "text") -> tuple[dict, list[dict]]:
    """Return (analysis summary, per-document checks)."""
    checks = check_rows(rows, source_key)
    result = {"overall": _support_stats(rows, checks), "baseline_metrics": summarize_run(rows)}
    by_trunc = {}
    for name, flag in (("truncated", True), ("not_truncated", False)):
        idx = [i for i, r in enumerate(rows) if bool(r["truncated"]) == flag]
        if idx:
            sub_rows = [rows[i] for i in idx]
            sub_checks = [checks[i] for i in idx]
            by_trunc[name] = {**_support_stats(sub_rows, sub_checks), "metrics": summarize_run(sub_rows)}
    result["by_truncation"] = by_trunc
    result["novel_rate_flag_threshold"] = NOVEL_RATE_FLAG
    result["source_key"] = source_key
    return result, checks


def review_sample(rows: list[dict], checks: list[dict], n_flagged: int = 30, n_control: int = 10,
                  seed: int = 42, snippet_chars: int = 400, source_key: str = "text") -> list[dict]:
    """Rows for manual labelling: flagged cases plus unflagged controls (to estimate false alarms)."""
    rng = random.Random(seed)
    flagged = [i for i, c in enumerate(checks) if is_flagged(c)]
    clean = [i for i, c in enumerate(checks) if not is_flagged(c)]
    pick = rng.sample(flagged, min(n_flagged, len(flagged))) + rng.sample(clean, min(n_control, len(clean)))
    out = []
    for i in pick:
        r, c = rows[i], checks[i]
        flags = []
        if c["unsupported_numbers"]:
            flags.append("numbers: " + " ".join(c["unsupported_numbers"]))
        if c["unsupported_dates"]:
            flags.append("dates: " + str(c["unsupported_dates"]))
        if c["novel_rate"] >= NOVEL_RATE_FLAG:
            flags.append(f"novel_rate: {c['novel_rate']}")
        out.append({
            "id": r["id"], "truncated": r["truncated"], "auto_flags": "; ".join(flags) or "none (control)",
            "reference": r["reference"], "prediction": r["prediction"],
            "source_start": r.get(source_key, r["text"])[:snippet_chars],
            "error_type": "", "notes": "",
        })
    return out
