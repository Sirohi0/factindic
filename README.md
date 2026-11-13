# FactIndic

Factuality-aware summarization for Indic and code-mixed text.
Semester project for NLP, Intelligent Model Design and MLOps (Bennett University).

## Status

Status updated 13 November 2026.

The 500-example Hindi mT5 baseline and a paired synthetic p100 code-mix baseline are complete, with predictions, metrics, truncation analysis, and rule-based checks saved under `results/`. A paired bootstrap comparison against the same Hindi references is in `results/paired_baseline_comparison.md`.

The controlled standard-vs-factuality-aware pilot has a 152-summary quality-filtered candidate, an assistant-only source-check pass, and a clean-source NLI re-score. Seven failed paired IDs were excluded symmetrically. Neither assistant screening nor NLI scores are human factuality labels. Human labels remain blank. The initial 28 terminal source-display markers were removed in a separate clean copy; row-by-row re-scoring found all NLI probabilities unchanged. See `results/factindic_interim_project_report_2026-11-13.md` and `results/ai_only_prompt_pilot_summary_2026-11-13.md`.

The current 7-slide teacher deck is `FactIndic_Progress_Checkpoint_2026-11-13_NLI_rescored.pptx` in the project root. It reports AI-only results, the clean-source re-score, and the MUTANT provenance limitations; revise it after human labels if annotation is completed.

## Foundation and attribution
- Summarization baseline: XL-Sum Hindi data and the mT5_multilingual_XLSum
  checkpoint, by Hasan et al. (2021), BUET CSE NLP Group. Not my work.
- Authentic code-mixed data: MUTANT (Gupta, Srivastava, and Singh, Findings of EACL 2023, DOI 10.18653/v1/2023.findings-eacl.56). The upstream dataset card declares CC BY 4.0. Of 50 PM-speech and Mankibaat candidates, 47 map uniquely by exact text match to an upstream file and 3 match two files; within the 30-example prompt pilot, 28 map uniquely and 2 are ambiguous. Original publisher/event URLs are not provided in the text files. See `scripts/map_mutant_provenance.py`, `results/mutant_source_provenance_audit_2026-11-13.md`, and `results/mutant_source_provenance_map_2026-11-13.csv`.
- Factuality methodology (later phase): inspired by factCC (Salesforce).
  I am adapting the idea, not using their trained English model.

## My contribution (in progress)
Baseline evaluation, error analysis, a Hindi/code-mixed factuality
verification approach, and MLOps tooling. Everything beyond the
foundation above is documented as my own work as it is done.

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

## Layout
| Path | Purpose |
| --- | --- |
| `src/factindic/config.py` | Pinned model and dataset revisions, generation settings |
| `src/factindic/data.py` | Loads the XL-Sum split from the pinned parquet revision |
| `src/factindic/baseline.py` | Inference-only baseline runner (resumable, per-document timing) |
| `src/factindic/metrics.py` | ROUGE precision/recall/F1, lengths, compression ratio, time |
| `src/factindic/text_utils.py` | Hindi-safe tokenizer, whitespace and digit helpers |
| `src/factindic/repro.py` | Records versions, device, git commit and sample ids per run |
| `scripts/` | `run_baseline.py`, `evaluate.py` |
| `scripts/summarize_assistant_prompt_review.py` | Rebuilds the descriptive assistant-only comparison from the review CSV; does not produce factuality gold labels |
| `scripts/analyze_nli_prompt_screening.py` | Verifies a Colab NLI ZIP against its input candidate and rebuilds matched prompt-arm score comparisons |
| `results/<run>/` | Run metadata, metrics, predictions, and analysis artifacts |
| `factindic_prompt_comparison_colab_revamped.ipynb` | Refreshed Colab prompt pilot with input checks, progress checkpoints, and diagnostic-vs-annotation export gating |
| `docs/factuality_annotation_protocol.md` | Human factuality labels and adjudication guidance |
| `docs/project_checkpoint_2026-11-13.md` | Current progress ladder, limitations, and next steps |
| `results/paired_baseline_comparison.md` | Paired ROUGE comparison with bootstrap intervals |
| `results/prompt_pilot_nli_rescore_2026-11-13/` | Clean-source Colab re-score, archive, row-level audit, and comparison with the original run |
| `results/factindic_interim_project_report_2026-11-13.md` | Current integrated project checkpoint and remaining work |
| `results/factindic_checkpoint_for_maam_2026-11-13.pdf` | Two-page supervisor brief with workflow, results, model rationale, and limits |

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
