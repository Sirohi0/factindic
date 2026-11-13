"""Turn Hindi text into Devanagari + English code-mixed text, and measure how mixed it is."""
from __future__ import annotations

import random
import re
import unicodedata

from .lexicon_hi_en import LEXICON

# Devanagari letters, vowel signs and nukta; excludes the danda (U+0964-0965) and Devanagari digits
_HI_RUN = re.compile(r"[\u0900-\u0963\u0970-\u097F]+")
_LATIN_RUN = re.compile(r"[A-Za-z]+")


def language_counts(text: str) -> tuple[int, int]:
    """(Hindi word runs, English word runs). Script decides the language; numbers and punctuation are ignored."""
    return len(_HI_RUN.findall(text)), len(_LATIN_RUN.findall(text))


def cmi(text: str) -> float:
    """Code-Mixing Index (Das and Gambaeck, 2014) for two languages: 100 * (1 - dominant share).
    0 means one language only; 50 is the maximum for two equally used languages."""
    hi, en = language_counts(text)
    n = hi + en
    return 0.0 if n == 0 else round(100 * (1 - max(hi, en) / n), 2)


def codemix_text(text: str, p: float, rng: random.Random, lexicon: dict | None = None) -> tuple[str, int]:
    """Replace each lexicon word with its English equivalent with probability p.
    Returns (code-mixed text, number of replacements). Deterministic for a given rng."""
    lexicon = LEXICON if lexicon is None else lexicon
    text = unicodedata.normalize("NFC", text)
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        word = m.group(0)
        en = lexicon.get(word)
        if en is not None and rng.random() < p:
            count += 1
            return en
        return word

    return _HI_RUN.sub(repl, text), count


def make_pair(doc_id: str, source: str, reference: str, p: float, seed: int = 42) -> dict:
    """Code-mix a source article and its reference summary with independent, reproducible choices."""
    text, n_src = codemix_text(source, p, random.Random(f"{seed}:{doc_id}:src"))
    summ, n_ref = codemix_text(reference, p, random.Random(f"{seed}:{doc_id}:ref"))
    return {
        "id": doc_id, "text": text, "summary": summ,
        "source_hi": source, "reference_hi": reference,
        "cmi_text": cmi(text), "cmi_summary": cmi(summ), "n_substitutions": n_src,
    }
