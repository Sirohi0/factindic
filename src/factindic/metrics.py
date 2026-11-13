"""Baseline metrics: ROUGE (precision, recall, F1), lengths, compression, time."""
from statistics import mean, median

from rouge_score import rouge_scorer

from .text_utils import WordTokenizer, tokenize

ROUGE_TYPES = ("rouge1", "rouge2", "rougeL")


def rouge_scores(predictions: list[str], references: list[str]) -> dict:
    """Mean ROUGE precision/recall/F1 (0-100) with a Hindi-safe tokenizer.

    The default rouge_score tokenizer keeps only [a-z0-9], so it would turn every
    Devanagari word into nothing and return 0. We pass our own tokenizer.
    Stemming is off: no Hindi stemmer is applied.
    """
    scorer = rouge_scorer.RougeScorer(list(ROUGE_TYPES), use_stemmer=False, tokenizer=WordTokenizer())
    sums = {t: {"precision": 0.0, "recall": 0.0, "fmeasure": 0.0} for t in ROUGE_TYPES}
    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        for t in ROUGE_TYPES:
            for k in ("precision", "recall", "fmeasure"):
                sums[t][k] += getattr(scores[t], k)
    n = max(len(predictions), 1)
    return {t: {k: round(100 * v / n, 2) for k, v in sums[t].items()} for t in ROUGE_TYPES}


def length_stats(predictions: list[str], references: list[str], sources: list[str]) -> dict:
    """Average lengths in words and compression ratio = summary words / source words."""
    p = [len(tokenize(x)) for x in predictions]
    r = [len(tokenize(x)) for x in references]
    s = [len(tokenize(x)) for x in sources]
    per_doc = [pl / sl for pl, sl in zip(p, s) if sl > 0]
    return {
        "avg_summary_words": round(mean(p), 2),
        "avg_reference_words": round(mean(r), 2),
        "avg_source_words": round(mean(s), 2),
        "compression_ratio_mean_per_doc": round(mean(per_doc), 4),
        "compression_ratio_corpus": round(sum(p) / sum(s), 4),
    }


def time_stats(seconds_per_doc: list[float]) -> dict:
    return {
        "inference_time_per_doc_s_mean": round(mean(seconds_per_doc), 3),
        "inference_time_per_doc_s_median": round(median(seconds_per_doc), 3),
    }


def summarize_run(rows: list[dict]) -> dict:
    """rows: records from predictions.jsonl (text, reference, prediction, gen_time_s, truncated)."""
    preds = [r["prediction"] for r in rows]
    refs = [r["reference"] for r in rows]
    srcs = [r["text"] for r in rows]
    out = {
        "n_documents": len(rows),
        "rouge": rouge_scores(preds, refs),
        **length_stats(preds, refs, srcs),
        **time_stats([r["gen_time_s"] for r in rows]),
        "share_inputs_truncated": round(sum(bool(r["truncated"]) for r in rows) / len(rows), 4),
    }
    if all("reference_hi" in r for r in rows):
        out["rouge_vs_hindi_reference"] = rouge_scores(preds, [r["reference_hi"] for r in rows])
    return out
