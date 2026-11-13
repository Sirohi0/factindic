"""Load an XL-Sum split from the pinned parquet revision."""
from __future__ import annotations
import pandas as pd

from .config import BaselineConfig


def load_split(cfg: BaselineConfig, n: int | None = None, seed: int = 42) -> pd.DataFrame:
    """Return the split with columns id, url, title, summary, text.

    If n is given, take a reproducible random sample (same seed, same documents),
    kept in the original order.
    """
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        cfg.dataset_name,
        f"{cfg.language}/{cfg.split}/0000.parquet",
        repo_type="dataset",
        revision=cfg.dataset_revision,
    )
    df = pd.read_parquet(path)
    df["id"] = df["id"].astype(str)
    if n is not None and n < len(df):
        df = df.sample(n=n, random_state=seed).sort_index()
    return df.reset_index(drop=True)
