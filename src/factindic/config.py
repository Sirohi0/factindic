"""Pinned settings for the Phase 1 baseline. Change these only on purpose:
every result file records the values that were in effect when it was produced."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BaselineConfig:
    # Foundation (credited to Hasan et al., 2021, BUET CSE NLP Group)
    model_name: str = "csebuetnlp/mT5_multilingual_XLSum"
    model_revision: str = "2437a524effdbadc327ced84595508f1e32025b3"
    dataset_name: str = "csebuetnlp/xlsum"
    dataset_revision: str = "ab04842511fc357feae53281fd104aa3c36dff07"  # refs/convert/parquet
    language: str = "hindi"
    split: str = "test"

    # Generation settings from the model card of the XL-Sum checkpoint
    max_input_tokens: int = 512
    max_summary_tokens: int = 84
    num_beams: int = 4
    no_repeat_ngram_size: int = 2


DEFAULT = BaselineConfig()
