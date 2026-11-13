"""Text helpers for Hindi, English and Hindi-English code-mixed text."""
import re
import unicodedata

_DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_WS = re.compile(r"\s+")


def clean_whitespace(text: str) -> str:
    """Same whitespace handling as the XL-Sum model card."""
    return _WS.sub(" ", text.strip())


def tokenize(text: str) -> list[str]:
    """Word tokenizer that works for Devanagari, Latin and mixed text.

    Why not a regex with \\w: in Python, Devanagari vowel signs (matras such as
    the one in "कि") are NOT alphanumeric, so \\w-based tokenizers split Hindi
    words apart. Instead we drop characters by Unicode category: punctuation
    and symbols (P*, S*, which includes the danda) become spaces, and invisible
    format characters (Cf, such as zero-width joiners) are deleted.
    Letters, combining marks and digits are kept.
    """
    text = unicodedata.normalize("NFC", text).lower()
    chars = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat == "Cf":
            continue
        chars.append(" " if cat[0] in "PSZC" else ch)
    return "".join(chars).split()


class WordTokenizer:
    """Adapter so rouge_score can use `tokenize` instead of its English-only default."""

    def tokenize(self, text: str) -> list[str]:
        return tokenize(text)


def normalize_digits(text: str) -> str:
    """Map Devanagari digits to ASCII (for the Phase 2 number checks)."""
    return text.translate(_DEVANAGARI_DIGITS)
