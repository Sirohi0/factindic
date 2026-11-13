"""Record everything needed to repeat a run."""
from __future__ import annotations
import platform
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from importlib import metadata

from .config import BaselineConfig

_PACKAGES = ("torch", "transformers", "huggingface_hub", "tokenizers", "sentencepiece",
             "pandas", "numpy", "rouge-score")


def _version(pkg: str) -> str:
    try:
        return metadata.version(pkg)
    except metadata.PackageNotFoundError:
        return "not installed"


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def collect_run_meta(cfg: BaselineConfig, *, n: int | None, seed: int, batch_size: int,
                     device: str, sample_ids: list[str], dry_run: bool) -> dict:
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "config": asdict(cfg),
        "sample": {"n": n, "seed": seed, "ids": sample_ids},
        "batch_size": batch_size,
        "device": device,
        "git_commit": _git_commit(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {p: _version(p) for p in _PACKAGES},
    }
