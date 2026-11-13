"""Run the XL-Sum mT5 baseline (inference only) and write one JSON line per document."""
import json
import time
from pathlib import Path

from .config import DEFAULT, BaselineConfig
from .text_utils import clean_whitespace


def pick_device(name: str = "auto") -> str:
    import torch

    if name != "auto":
        return name
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class MT5Summarizer:
    """Callable: list of texts -> list of {prediction, input_tokens, truncated}.

    Uses the settings from the model card of the XL-Sum checkpoint
    (beam search, no_repeat_ngram_size=2, 512 input / 84 output tokens).
    """

    def __init__(self, cfg: BaselineConfig = DEFAULT, device: str = "auto"):
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.torch = torch
        self.cfg = cfg
        self.device = pick_device(device)
        self.tok = AutoTokenizer.from_pretrained(cfg.model_name, revision=cfg.model_revision)
        self.model = (
            AutoModelForSeq2SeqLM.from_pretrained(cfg.model_name, revision=cfg.model_revision)
            .to(self.device)
            .eval()
        )

    def _sync(self):
        if self.device.startswith("cuda"):
            self.torch.cuda.synchronize()
        elif self.device == "mps":
            self.torch.mps.synchronize()

    def __call__(self, texts: list[str]) -> list[dict]:
        cfg = self.cfg
        full_len = [len(ids) for ids in self.tok(texts, add_special_tokens=True, truncation=False)["input_ids"]]
        enc = self.tok(
            texts, return_tensors="pt", padding=True, truncation=True, max_length=cfg.max_input_tokens
        ).to(self.device)
        with self.torch.inference_mode():
            out = self.model.generate(
                input_ids=enc["input_ids"],
                attention_mask=enc["attention_mask"],
                max_length=cfg.max_summary_tokens,
                num_beams=cfg.num_beams,
                no_repeat_ngram_size=cfg.no_repeat_ngram_size,
            )
        self._sync()
        preds = self.tok.batch_decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        return [
            {"prediction": p, "input_tokens": n, "truncated": n > cfg.max_input_tokens}
            for p, n in zip(preds, full_len)
        ]


def read_rows(path: Path) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run_baseline(summarize, df, out_path: Path, batch_size: int = 1, log_every: int = 10) -> None:
    """Summarize every document in df that is not already in out_path (resumable).

    Each line stores the text the model was given (whitespace-cleaned, before
    truncation), the reference, the prediction, token counts, a truncated flag,
    and the generation time per document (batch time / batch size).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = {r["id"] for r in read_rows(out_path)}
    todo = df[~df["id"].astype(str).isin(done)]
    print(f"{len(done)} already done, {len(todo)} to run")

    with open(out_path, "a", encoding="utf-8") as f:
        for b, start in enumerate(range(0, len(todo), batch_size)):
            chunk = todo.iloc[start : start + batch_size]
            texts = [clean_whitespace(t) for t in chunk["text"]]
            t0 = time.perf_counter()
            outs = summarize(texts)
            per_doc = (time.perf_counter() - t0) / len(chunk)
            for (_, row), text, out in zip(chunk.iterrows(), texts, outs):
                record = {
                    "id": str(row["id"]),
                    "text": text,
                    "reference": row["summary"],
                    "prediction": out["prediction"],
                    "input_tokens": out["input_tokens"],
                    "truncated": out["truncated"],
                    "gen_time_s": round(per_doc, 4),
                }
                for extra in ("reference_hi", "source_hi"):  # present for code-mixed datasets
                    if extra in chunk.columns:
                        record[extra] = row[extra]
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            if (b + 1) % log_every == 0:
                print(f"  {start + len(chunk)}/{len(todo)} documents")
