from factindic.checks import check_summary, extract_dates, extract_numbers, novel_tokens


def test_numbers_devanagari_and_grouping():
    assert extract_numbers("२०२४ में 1,20,000 लोग और 2.5 प्रतिशत") == ["2024", "120000", "2.5"]


def test_number_list_not_merged():
    assert extract_numbers("1,2 और 3") == ["1", "2", "3"]


def test_dates_hindi_and_english():
    assert extract_dates("15 अगस्त 2024 को") == [(15, 8)]
    assert extract_dates("on 3 october and december") == [(3, 10), (None, 12)]


def test_nukta_month_is_recognised():
    assert extract_dates("12 फ़रवरी") == [(12, 2)]


def test_ambiguous_english_months_ignored():
    assert extract_dates("may march 5") == []


def test_supported_numbers_pass():
    src = "टीम ने रविवार को 3 रन से जीत दर्ज की। कप्तान ने 120 रन बनाए।"
    c = check_summary(src, "कप्तान ने १२० रन बनाए")
    assert c["unsupported_numbers"] == []


def test_changed_number_is_flagged():
    src = "कप्तान ने 120 रन बनाए।"
    c = check_summary(src, "कप्तान ने 150 रन बनाए")
    assert c["unsupported_numbers"] == ["150"]


def test_changed_date_is_flagged_but_same_date_passes():
    src = "यह घटना 15 अगस्त को हुई।"
    assert check_summary(src, "घटना 16 अगस्त को हुई")["unsupported_dates"] == [(16, 8)]
    assert check_summary(src, "घटना 15 अगस्त को हुई")["unsupported_dates"] == []


def test_novel_tokens_ignore_short_words_and_digits():
    out = novel_tokens("सरकार ने 5 नई योजना बनाई", "सरकार ने योजना बनाई")
    assert out == []  # "नई" is only 2 code points ("न", "ई") so below min_len
    assert novel_tokens("सरकार ने नया कानून बनाया", "सरकार ने योजना बनाई") == ["नया", "कानून", "बनाया"]


def test_novel_rate():
    c = check_summary("सरकार ने योजना बनाई", "सरकार ने नया कानून")
    assert c["novel_rate"] == round(2 / 4, 4)
