# FactIndic

Factuality-aware summarization for Indic and code-mixed text.
Semester project for NLP, Intelligent Model Design and MLOps (Bennett University).

## Status

Status updated 18 November 2026 (including **Dual-Archetype Guarded Re-Evaluation**).

[![Open final pilot in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_final_open_hinglish_colab.ipynb)

**Dual-Archetype Guarded Re-Evaluation (240 outputs, Colab T4):** `factindic_dual_archetype_reeval_colab.ipynb` re-evaluated the full guarded pipeline (pure greedy decoding, deterministic `extract_fact_anchors`, verbatim quote verification, Hinglish NLI gloss normalization, and `NLI_CONTRADICTION_THRESHOLD = 0.85`) across **30 Roman-script Hinglish** (`News_Hinglish_English`) and **30 Devanagari/Code-Mixed** (`XL-Sum Hindi` `p=1.0`) articles × 4 conditions (`results/dual_archetype_reeval_summary.json`):
- **Roman-Script Hinglish:** Error rates dropped by **23.4–36.6 pp** vs. the original pilot—`Qwen3 1.7B Standard`: `56.7%` (`13/30` supported, **−36.6 pp**), `Qwen3 1.7B Factuality-aware`: `63.3%` (`11/30` supported, **−23.4 pp**), `Qwen3 4B Standard`: `46.7%` (`16/30` supported, `2` minor, `12` major, **−33.3 pp**, `53.3%` pass rate), `Qwen3 4B Factuality-aware`: `50.0%` (`15/30` supported, `2` minor, `13` major, **−26.7 pp**).
- **Devanagari / Code-Mixed (`XL-Sum` `p=1.0`):** On long multi-paragraph articles (`0.2245–0.2443` compression), strict quote/NLI checks flagged `100.0%` (`1.7B`), `96.7%` (`4B Standard`, `1/30` supported), and `93.3%` (`4B Factuality-aware`, `2/30` supported, `3` minor).

**Final Roman-script Hinglish pilot (17 November):** the public `News_Hinglish_English` dataset was used after the teacher approved any dataset. The GPU run completed on 30 sources and produced 120 summaries across Qwen3-1.7B/Qwen3-4B and standard/factuality-aware prompts. The dataset's Hinglish side is machine-generated and curated, and it has no gold summaries, so ROUGE is not reported. A separate AI-assisted source comparison flagged 74 major errors, 27 minor errors, and 19 supported summaries; these are provisional AI judgments, not human factuality labels. The run is exploratory and establishes no prompt winner. Human validation is intentionally skipped for this version. The final run also exports per-condition summary length, compression, and generation-time metrics. Aggregate results are recorded in [`results/final_hinglish_generation_metrics_2026-11-18.md`](results/final_hinglish_generation_metrics_2026-11-18.md) and the companion CSV; no row-level source or summary text is published. See the [AI-screening report](docs/final_hinglish_ai_screening_report_2026-11-17.md), [run checkpoint](docs/final_hinglish_run_plan_2026-11-17.md), and [Colab notebook](factindic_final_open_hinglish_colab.ipynb).

**Dataset-scope correction:** the intended code-mixed target is Roman-script
Hinglish (Hindi transliterated into Latin letters, mixed with English). An audit
found that none of the 76 sources in the earlier prompt pilot used this script
style; the pilot was Devanagari-based. Keep those results as exploratory prior
work, not as evidence about Roman-script Hinglish. The corrected data plan and
access requirement are documented in
[`docs/dataset_scope_correction_2026-11-13.md`](docs/dataset_scope_correction_2026-11-13.md).

The 500-example Hindi mT5 baseline and a paired synthetic p100 code-mix baseline are complete, with predictions, metrics, truncation analysis, and rule-based checks saved under `results/`. A paired bootstrap comparison against the same Hindi references is in `results/paired_baseline_comparison.md`.

The earlier controlled standard-vs-factuality-aware pilot has a 152-summary quality-filtered candidate, assistant-only source checks, and a clean-source NLI re-score. It does not match the intended Roman-script Hinglish style: all 76 unique sources are Devanagari-based. Keep these results exploratory and do not annotate the old review sheet as the target Hinglish evaluation. Neither assistant screening nor NLI scores are human factuality labels. See `docs/dataset_scope_correction_2026-11-13.md` before using prior code-mix results.

The final teacher-facing deliverables are the [IEEE research paper PDF](docs/final_submission/FactIndic_Research_Paper_Final_2026-11-18.pdf), [editable IEEE paper DOCX](docs/final_submission/FactIndic_Research_Paper_Final_2026-11-18.docx), [final project report](docs/final_submission/FactIndic_Project_Report_Final_2026-11-18.pdf) ([Markdown](docs/final_submission/FactIndic_Project_Report_Final_2026-11-18.md) / [DOCX](docs/final_submission/FactIndic_Project_Report_Final_2026-11-18.docx)), and [nine-slide presentation](docs/final_submission/FactIndic_Final_Presentation_Final_2026-11-18.pptx). They include the final generation metrics, interactive pipeline architecture, and distinguish AI screening from human validation. The 17 November checkpoint and 13 November scope-correction deck/PDF remain historical context.

A gated GupShup alternative remains in `factindic_romanized_hinglish_colab.ipynb`. The current final path is `factindic_final_open_hinglish_colab.ipynb`, which pins the public Romanized Hinglish news corpus, runs a paired two-size/two-prompt comparison, and exports a private blinded factuality worksheet. Since the corpus has no gold summaries, the notebook intentionally omits ROUGE. AI-assisted labels are exported with explicit AI metadata and remain separate from human evaluation.

## Foundation and attribution
- Summarization baseline: XL-Sum Hindi data and the mT5_multilingual_XLSum
  checkpoint, by Hasan et al. (2021), BUET CSE NLP Group. Not my work.
- Earlier code-mix data exploration: MUTANT (Gupta, Srivastava, and Singh, Findings of EACL 2023, DOI 10.18653/v1/2023.findings-eacl.56). Its sampled items in this project are Devanagari-based, so they do not satisfy the corrected Roman-script Hinglish target. Of 50 PM-speech and Mankibaat candidates, 47 map uniquely by exact text match to an upstream file and 3 match two files; within the 30-example prompt pilot, 28 map uniquely and 2 are ambiguous. See `scripts/map_mutant_provenance.py` and `results/mutant_source_provenance_audit_2026-11-13.md`.
- GupShup h2e remains a better fit if access is granted because it includes reference summaries; its access request is pending and no data is present locally.
- Current final data path: `suyash2739/News_Hinglish_English`, a public English/Romanized-Hinglish news parallel corpus, pinned in the final Colab notebook. The Hinglish side is machine-generated and curated, and the dataset contains translations rather than summary references. The final generation run is complete; human factuality review has not been completed.
- Factuality approach: a source-grounded AI-assisted screen informed by FactCC, SummaC, and FActScore. It is an exploratory, unvalidated signal; this project does not use the trained FactCC English model or claim human-verified factuality.

## My contribution (in progress)
Baseline evaluation, error analysis, a Hindi/code-mixed factuality
verification approach, and MLOps tooling. Everything beyond the
foundation above is documented as my own work as it is done.

## Live project evaluation

Use the [interactive FactIndic Colab notebook](https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_interactive_evaluation_colab.ipynb) to test one source at a time. Select a T4 GPU runtime, run its cells, paste Roman-script Hinglish text, and choose **Summarize and check claims**. It runs pure greedy Qwen3 decoding (without `repetition_penalty` or `no_repeat_ngram_size`, which previously caused ±1 digit shifts), returns an English summary, verifies extracted evidence quotes verbatim against the model-visible source, and adds a secondary cross-lingual NLI signal (`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`). A number/date mismatch triggers one constrained summary retry; remaining date/name corrections are disclosed, and any unresolved mismatch, unverified quote, or NLI contradiction keeps the output labeled as an unverified draft. Because `mDeBERTa-v3-base-mnli-xnli` is trained on Devanagari Hindi/English XNLI rather than Roman-script Hinglish, treat both AI and NLI outputs as unvalidated review aids.

The fixed 30-source research comparison is in the [final experiment notebook](https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_final_open_hinglish_colab.ipynb). The Mac app is a local results viewer; the interactive evaluation runs in Colab.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
pytest                                        # unit tests, no download needed
python scripts/run_baseline.py --dry-run      # pipeline check, no model
python scripts/run_baseline.py --n 50         # first real run (downloads the model once)
python scripts/evaluate.py results/<run>/predictions.jsonl   # recompute metrics only
```
If `--device mps` fails on a Mac, use `--device cpu`. Runs are resumable: repeat
the same command and finished documents are skipped.

## Native macOS frontend

The local SwiftUI app is in `macos/FactIndicApp/`. It presents the Hindi paired
baseline, AI-screened pilot comparisons, per-condition generation metrics, methods, and limitations. It is a results
viewer only: it does not run models, training, or factuality verification on the
Mac. The displayed labels are AI-assisted screening, not human-verified results.

Build and launch the Mac app from the repository root:

```bash
./macos/FactIndicApp/build-macos-app.sh
open macos/FactIndicApp/FactIndic.app
```

## Where to Find What (Repository Map)

| Path | Purpose |
| --- | --- |
| `docs/final_submission/` | **Teacher-facing deliverables:** IEEE paper (`.docx`/`.pdf`), project report (`.md`/`.docx`/`.pdf`), 9-slide presentation (`.pptx`). |
| `factindic_interactive_evaluation_colab.ipynb` | **Live Colab T4 demo:** Dual-archetype (`Auto-detect`, Roman Hinglish, Devanagari/Code-Mixed) summary + claim-level evidence + `mDeBERTa` NLI. |
| `factindic_dual_archetype_reeval_colab.ipynb` | **Dual-archetype guarded re-eval:** 240-output benchmark across Roman Hinglish (`News_Hinglish_English`) and Devanagari (`XL-Sum p=1.0`). |
| `factindic_final_open_hinglish_colab.ipynb` | **Original Roman Hinglish pilot:** 120-summary paired comparison (`Qwen3 1.7B/4B` × `Standard/Factuality-aware`). |
| `macos/FactIndicApp/` | **Native macOS SwiftUI viewer:** Browse baselines, dual-archetype guarded results, generation metrics, and run `51` unit tests. |
| `src/factindic/` | Core Python package (`config`, `data`, `baseline`, `checks`, `codemix`, `metrics`, `analysis`, `text_utils`, `repro`). |
| `scripts/` | CLI runners & audits (`run_baseline.py`, `evaluate.py`, `make_codemixed.py`, `analyze.py`, `map_mutant_provenance.py`). |
| `tests/` | `51` fast local unit & notebook-contract tests (`pytest`, runs in `~0.5s` with no GPU). |
| `results/` | Saved aggregate metrics (`dual_archetype_reeval_summary.json`, `paired_baseline_comparison.md`, `final_hinglish_generation_metrics_2026-11-18.md`). |
| `docs/checkpoints/` | Dated engineering checkpoints, scope-correction audit, and AI-screening notes. |
| `docs/archive/presentations/` | Historical milestone & scope-correction slide decks (`FactIndic_Scope_Correction_2026-11-13.pptx`, etc.). |
| `notebooks/archive/` | Earlier Devanagari prompt-comparison, NLI screening, and gated GupShup `h2e` notebooks. |

## Prompt-pilot NLI screening

`factindic_prompt_nli_screening_colab.ipynb` scores the quality-filtered 152-summary prompt pilot using the existing multilingual NLI checkpoint. It consumes the candidate ZIP under `results/prompt_pilot_review_candidate_2026-11-09/` and exports per-summary scores, descriptive and within-document paired prompt-arm aggregates, model/run metadata, and the original blank review sheet. The clean-source re-score input and verified Colab output are archived under `results/prompt_pilot_nli_rescore_2026-11-13/`. Run it in Colab with a GPU; it does not regenerate summaries. NLI scores are exploratory model signals, not factuality labels or replacements for human review.

## Metric definitions
- **ROUGE**: precision, recall and F1 for ROUGE-1/2/L, using our own tokenizer (the
  default `rouge_score` tokenizer scores Devanagari as empty). No stemming. These
  numbers are not guaranteed to match the XL-Sum paper's, which uses its own
  multilingual ROUGE; do not call a run "reproduced" without checking that.
- **Average summary length**: words per summary, same tokenizer.
- **Compression ratio**: summary words divided by source words (mean per document and corpus-level).
- **Inference time**: seconds per document after one untimed warm-up, on the device recorded in `run_meta.json`.
- **Truncation**: inputs longer than 512 tokens are cut. `truncated` is recorded per
  document; later verification must check summaries against what the model actually saw.
