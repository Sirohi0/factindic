from factindic.text_utils import clean_whitespace, normalize_digits, tokenize


def test_hindi_words_are_not_split_at_vowel_signs():
    toks = tokenize("भारत में प्रदूषण का स्तर लगातार बढ़ रहा है।")
    assert len(toks) == 9
    assert "प्रदूषण" in toks
    assert toks[-1] == "है"  # danda removed, word intact


def test_ki_keeps_its_matra():
    assert tokenize("क्या कि") == ["क्या", "कि"]


def test_code_mixed_sentence():
    toks = tokenize("भारत में pollution का level लगातार increase हो रहा है।")
    assert toks == ["भारत", "में", "pollution", "का", "level", "लगातार", "increase", "हो", "रहा", "है"]


def test_latin_is_lowercased_and_punctuation_dropped():
    assert tokenize("Climate Change, ki wajah!") == ["climate", "change", "ki", "wajah"]


def test_zero_width_joiner_is_deleted():
    assert tokenize("क\u200dष") == tokenize("कष")


def test_normalize_digits():
    assert normalize_digits("२०२४ में 120 रन") == "2024 में 120 रन"


def test_clean_whitespace():
    assert clean_whitespace("  a \n\n b\t c ") == "a b c"
