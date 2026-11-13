import pytest

from factindic.metrics import length_stats, rouge_scores, summarize_run


def test_identical_hindi_text_scores_100():
    s = "भारत में प्रदूषण बढ़ रहा है"
    r = rouge_scores([s], [s])
    assert r["rouge1"]["fmeasure"] == 100.0
    assert r["rougeL"]["fmeasure"] == 100.0


def test_devanagari_is_not_scored_as_empty():
    """The default rouge_score tokenizer returns 0 for Devanagari; ours must not."""
    r = rouge_scores(["भारत में प्रदूषण"], ["भारत में प्रदूषण बढ़ रहा"])
    assert r["rouge1"]["fmeasure"] > 0


def test_precision_and_recall_are_separate():
    r = rouge_scores(["भारत में प्रदूषण"], ["भारत में प्रदूषण बढ़ रहा"])
    assert r["rouge1"]["precision"] == 100.0
    assert r["rouge1"]["recall"] == 60.0


def test_disjoint_text_scores_zero():
    assert rouge_scores(["सरकार योजना"], ["टीम मैच जीता"])["rouge1"]["fmeasure"] == 0.0


def test_compression_ratio():
    st = length_stats(["एक दो"], ["एक दो तीन"], ["एक दो तीन चार पांच छह सात आठ नौ दस"])
    assert st["compression_ratio_corpus"] == pytest.approx(0.2)
    assert st["avg_summary_words"] == 2.0


def test_summarize_run_keys():
    rows = [{"text": "एक दो तीन चार", "reference": "एक दो", "prediction": "एक दो",
             "gen_time_s": 0.5, "truncated": False}]
    m = summarize_run(rows)
    assert m["n_documents"] == 1
    assert m["rouge"]["rouge1"]["fmeasure"] == 100.0
    assert m["share_inputs_truncated"] == 0.0
