import random
import unicodedata

from factindic.checks import extract_dates, extract_numbers
from factindic.codemix import cmi, codemix_text, language_counts, make_pair
from factindic.lexicon_hi_en import LEXICON

TEXT = "भारत में प्रदूषण का स्तर लगातार बढ़ रहा है। सरकार ने 2024 में योजना शुरू की। मंत्री ने 15 अगस्त को बयान दिया।"


def test_lexicon_is_clean():
    assert len(LEXICON) > 200
    assert all(k == unicodedata.normalize("NFC", k) and v for k, v in LEXICON.items())


def test_cmi_values():
    assert cmi("भारत में प्रदूषण है") == 0.0
    assert cmi("pollution level") == 0.0
    assert cmi("pollution का level") == round(100 * (1 - 2 / 3), 2)
    assert cmi("") == 0.0


def test_language_counts_ignore_digits_and_danda():
    assert language_counts("२०२४ 15 । भारत") == (1, 0)


def test_p_zero_changes_nothing_and_p_one_swaps_known_words():
    out0, n0 = codemix_text(TEXT, 0.0, random.Random(1))
    assert out0 == unicodedata.normalize("NFC", TEXT) and n0 == 0
    out1, n1 = codemix_text(TEXT, 1.0, random.Random(1))
    assert "pollution" in out1 and "level" in out1 and "government" in out1 and n1 >= 5
    assert "भारत" in out1  # not in the lexicon, so untouched


def test_facts_are_preserved():
    out, _ = codemix_text(TEXT, 1.0, random.Random(1))
    assert extract_numbers(out) == extract_numbers(TEXT)
    assert extract_dates(out) == extract_dates(TEXT)


def test_deterministic_and_paired():
    a = make_pair("d1", TEXT, "प्रदूषण का स्तर बढ़ रहा है", 0.5, seed=7)
    b = make_pair("d1", TEXT, "प्रदूषण का स्तर बढ़ रहा है", 0.5, seed=7)
    assert a == b
    assert a["source_hi"] == TEXT and a["reference_hi"] == "प्रदूषण का स्तर बढ़ रहा है"
    assert 0 < a["cmi_text"] <= 50


def test_danda_is_kept():
    out, _ = codemix_text("सरकार ने फैसला किया।", 1.0, random.Random(1))
    assert out == "government ने decision किया।"
