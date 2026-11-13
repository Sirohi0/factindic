import pandas as pd

from factindic.baseline import read_rows, run_baseline


def frame():
    return pd.DataFrame({
        "id": ["a", "b", "c"],
        "summary": ["एक", "दो", "तीन"],
        "text": ["एक  दो\nतीन", "चार पांच", "छह सात आठ"],
    })


def stub(texts):
    return [{"prediction": t.split()[0], "input_tokens": len(t.split()), "truncated": False} for t in texts]


def test_writes_one_row_per_document(tmp_path):
    p = tmp_path / "p.jsonl"
    run_baseline(stub, frame(), p, batch_size=2)
    rows = read_rows(p)
    assert [r["id"] for r in rows] == ["a", "b", "c"]
    assert rows[0]["text"] == "एक दो तीन"  # whitespace cleaned
    assert all(r["gen_time_s"] >= 0 for r in rows)


def test_resume_does_not_duplicate(tmp_path):
    p = tmp_path / "p.jsonl"
    run_baseline(stub, frame().iloc[:2], p)
    run_baseline(stub, frame(), p)
    assert sorted(r["id"] for r in read_rows(p)) == ["a", "b", "c"]


def test_extra_columns_and_hindi_reference_metrics(tmp_path):
    from factindic.metrics import summarize_run

    df = frame()
    df["reference_hi"] = ["एक", "दो", "तीन"]
    df["source_hi"] = ["एक दो तीन", "चार पांच", "छह सात आठ"]
    p = tmp_path / "p.jsonl"
    run_baseline(stub, df, p)
    rows = read_rows(p)
    assert rows[0]["reference_hi"] == "एक" and rows[0]["source_hi"] == "एक दो तीन"
    assert "rouge_vs_hindi_reference" in summarize_run(rows)
