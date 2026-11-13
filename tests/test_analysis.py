from factindic.analysis import analyze_rows, is_flagged, review_sample, check_rows


def row(i, text, ref, pred, truncated=False):
    return {"id": i, "text": text, "reference": ref, "prediction": pred, "truncated": truncated,
            "gen_time_s": 1.0, "input_tokens": 10}


ROWS = [
    row("a", "कप्तान ने 120 रन बनाए। टीम जीती।", "कप्तान ने 120 रन बनाए", "कप्तान ने 120 रन बनाए"),
    row("b", "कप्तान ने 120 रन बनाए। टीम जीती।", "कप्तान ने 120 रन बनाए", "कप्तान ने 150 रन बनाए", True),
    row("c", "सरकार ने योजना शुरू की।", "सरकार ने योजना शुरू की", "सरकार ने योजना शुरू की", True),
]


def test_aggregates():
    res, checks = analyze_rows(ROWS)
    o = res["overall"]
    assert o["n_documents"] == 3
    assert o["summaries_with_numbers"] == 2
    assert o["docs_with_unsupported_number"] == 1
    assert o["number_support_rate"] == 0.5  # 120 supported, 150 not
    assert o["number_preservation_rate"] == 0.5  # reference has 120 twice; kept once
    assert o["docs_flagged"] == 1


def test_split_by_truncation():
    res, _ = analyze_rows(ROWS)
    assert res["by_truncation"]["truncated"]["n_documents"] == 2
    assert res["by_truncation"]["not_truncated"]["n_documents"] == 1
    assert res["by_truncation"]["truncated"]["docs_flagged"] == 1


def test_review_sample_has_flagged_and_control_and_blank_labels():
    _, checks = analyze_rows(ROWS)
    sample = review_sample(ROWS, checks, n_flagged=5, n_control=1, seed=1)
    ids = [s["id"] for s in sample]
    assert "b" in ids and len(sample) == 2
    assert all(s["error_type"] == "" and s["notes"] == "" for s in sample)
    assert any(s["auto_flags"].startswith("none") for s in sample)


def test_is_flagged_uses_threshold():
    c = check_rows([row("x", "सरकार ने योजना बनाई", "x", "नया कानून पारित हुआ")])[0]
    assert is_flagged(c)


def test_source_key_switches_the_source_used():
    r = row("z", "government ने 150 रन गिने", "x", "सरकार ने 120 रन गिने")
    r["source_hi"] = "सरकार ने 120 रन गिने"
    from factindic.analysis import check_rows
    assert check_rows([r], "text")[0]["unsupported_numbers"] == ["120"]
    assert check_rows([r], "source_hi")[0]["unsupported_numbers"] == []
