"""Rule-based support checks for Phase 2 failure analysis.

These are screening tools, not verdicts. They find numbers, dates and words in a
summary that cannot be matched to the source, so a human can then label real errors.

Known limits (state them when you present results):
- Numbers written as words ("तीन") are not detected, only digits.
- Hindi is inflected, so a word that differs only by suffix counts as "novel".
- The source is the full cleaned article; the model only saw its first 512 tokens.
- English "march" and "may" are not treated as months (too ambiguous).
"""
from __future__ import annotations

import re
import unicodedata

from .text_utils import normalize_digits, tokenize

# digits with optional Western (1,000) or Indian (1,00,000) grouping and decimals
_NUM = re.compile(r"\d+(?:,\d{2,3})*(?:\.\d+)?")

_MONTHS_RAW = {
    "जनवरी": 1, "फरवरी": 2, "फ़रवरी": 2, "मार्च": 3, "अप्रैल": 4, "मई": 5, "जून": 6, "जुलाई": 7,
    "अगस्त": 8, "सितंबर": 9, "सितम्बर": 9, "अक्टूबर": 10, "अक्तूबर": 10, "नवंबर": 11, "नवम्बर": 11,
    "दिसंबर": 12, "दिसम्बर": 12,
    "january": 1, "february": 2, "april": 4, "june": 6, "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}
MONTHS = {unicodedata.normalize("NFC", k): v for k, v in _MONTHS_RAW.items()}


def extract_numbers(text: str) -> list[str]:
    """All numbers as ASCII strings without thousands separators (Devanagari digits converted)."""
    return [m.replace(",", "") for m in _NUM.findall(normalize_digits(text))]


def extract_dates(text: str) -> list[tuple]:
    """(day or None, month) for each month name found; day is a 1-31 number next to the month."""
    toks = tokenize(normalize_digits(text))
    out = []
    for i, t in enumerate(toks):
        if t in MONTHS:
            day = None
            for j in (i - 1, i + 1):
                if 0 <= j < len(toks) and toks[j].isdigit() and 1 <= int(toks[j]) <= 31:
                    day = int(toks[j])
                    break
            out.append((day, MONTHS[t]))
    return out


def novel_tokens(summary: str, source: str, min_len: int = 3) -> list[str]:
    """Summary words (not digits) that never occur in the source."""
    src = set(tokenize(source))
    return [t for t in tokenize(summary) if t not in src and len(t) >= min_len and not t.isdigit()]


def check_summary(source: str, summary: str) -> dict:
    src_nums = set(extract_numbers(source))
    pred_nums = extract_numbers(summary)
    src_dates = extract_dates(source)
    pred_dates = extract_dates(summary)
    unsupported_dates = [
        d for d in pred_dates
        if not any(s[1] == d[1] and (d[0] is None or s[0] == d[0]) for s in src_dates)
    ]
    novel = novel_tokens(summary, source)
    n_tokens = max(len(tokenize(summary)), 1)
    return {
        "numbers": pred_nums,
        "unsupported_numbers": [n for n in pred_nums if n not in src_nums],
        "dates": pred_dates,
        "unsupported_dates": unsupported_dates,
        "novel_tokens": novel,
        "novel_rate": round(len(novel) / n_tokens, 4),
    }
