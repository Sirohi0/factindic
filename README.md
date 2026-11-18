# FactIndic

Factuality-aware summarization for Indic and code-mixed text.
Semester project for NLP, Intelligent Model Design and MLOps (Bennett University).

## Status

Status updated 18 November 2026.

[![Open final pilot in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_final_open_hinglish_colab.ipynb)

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

The final teacher-facing deliverables are the [research paper PDF](docs/final_submission/FactIndic_Research_Paper_Final_2026-11-18.pdf), [editable paper DOCX](docs/final_submission/FactIndic_Research_Paper_Final_2026-11-18.docx), and [nine-slide presentation](docs/final_submission/FactIndic_Final_Presentation_Final_2026-11-18.pptx). They include the final generation metrics and distinguish AI screening from human validation. The 17 November checkpoint and 13 November scope-correction deck/PDF remain historical context.

A gated GupShup alternative remains in `factindic_romanized_hinglish_colab.ipynb`. The current final path is `factindic_final_open_hinglish_colab.ipynb`, which pins the public Romanized Hinglish news corpus, runs a paired two-size/two-prompt comparison, and exports a private blinded factuality worksheet. Since the corpus has no gold summaries, the notebook intentionally omits ROUGE. AI-assisted labels are exported with explicit AI metadata and remain separate from human evaluation.

## Foundation and attribution
- Summarization baseline: XL-Sum Hindi data and the mT5_multilingual_XLSum
  checkpoint, by Hasan et al. (2021), BUET CSE NLP Group. Not my work.
- Earlier code-mix data exploration: MUTANT (Gupta, Srivastava, and Singh, Findings of EACL 2023, DOI 10.18653/v1/2023.findings-eacl.56). Its sampled items in this project are Devanagari-based, so they do not satisfy the corrected Roman-script Hinglish target. Of 50 PM-speech and Mankibaat candidates, 47 map uniquely by exact text match to an upstream file and 3 match two files; within the 30-example prompt pilot, 28 map uniquely and 2 are ambiguous. See `scripts/map_mutant_provenance.py` and `results/mutant_source_provenance_audit_2026-11-13.md`.
- GupShup h2e remains a better fit if access is granted because it includes reference summaries; its access request is pending and no data is present locally.
- Current final data path: `suyash2739/News_Hinglish_English`, a public English/Romanized-Hinglish news parallel corpus, pinned in the final Colab notebook. The Hinglish side is machine-generated and curated, and the dataset contains translations rather than summary references. The final generation run is complete; human factuality review has not been completed.
- Factuality approach: a source-grounded AI-assisted screen informed by factCC.
  It is an exploratory, unvalidated signal; this project does not use the trained
  FactCC English model or claim human-verified factuality.

## My contribution (in progress)
Baseline evaluation, error analysis, a Hindi/code-mixed factuality
verification approach, and MLOps tooling. Everything beyond the
foundation above is documented as my own work as it is done.

## Live project evaluation

Use the [interactive FactIndic Colab notebook](https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_interactive_evaluation_colab.ipynb) to test one source at a time. Select a T4 GPU runtime, run its cells, paste Roman-script Hinglish text, and choose **Summarize and check claims**. It returns an English summary and a claim table with AI assessments and source quotes. Accepted quotes are checked against the model-visible source. A number/date mismatch triggers one constrained summary retry. A remaining date mismatch is corrected only when one unique full date appears in both source and summary; ambiguous or unresolved date/number mismatches are marked as unsafe drafts. The model’s support judgment is still AI-assisted and unvalidated, so treat the output as a review aid.

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
| `scripts/audit_romanized_parallel.py` | Checks paired source/reference alignment and Roman/Devanagari script counts for private GupShup h2e files; it does not replace manual Hinglish review |
| `results/<run>/` | Run metadata, metrics, predictions, and analysis artifacts |
| `factindic_prompt_comparison_colab_revamped.ipynb` | Refreshed Colab prompt pilot with input checks, progress checkpoints, and diagnostic-vs-annotation export gating |
| `factindic_romanized_hinglish_colab.ipynb` | Corrected GupShup h2e Roman-script pilot: 30 paired test sources, two multilingual 4B models, two prompts, blind human factuality review, paired ROUGE bootstrap |
| `factindic_final_open_hinglish_colab.ipynb` | Final-run Colab: 30 Roman-script Hinglish news inputs × two Qwen3 sizes × two prompts, private review workflow, per-condition generation metrics, no ROUGE because no gold summaries |
| `factindic_interactive_evaluation_colab.ipynb` | Live Colab demonstration: paste one Roman-script Hinglish source, generate an English summary, and inspect claim-level source evidence |
| `docs/factuality_annotation_protocol.md` | Human factuality labels and adjudication guidance |
| `docs/project_checkpoint_2026-11-13.md` | Current progress ladder, limitations, and next steps |
| `docs/dataset_scope_correction_2026-11-13.md` | Corrected Roman-script Hinglish target, existing-data audit, and replacement plan |
| `results/paired_baseline_comparison.md` | Paired ROUGE comparison with bootstrap intervals |
| `results/prompt_pilot_nli_rescore_2026-11-13/` | Clean-source Colab re-score, archive, row-level audit, and comparison with the original run |
| `results/factindic_interim_project_report_2026-11-13.md` | Current integrated project checkpoint and remaining work |
| `FactIndic_Scope_Correction_2026-11-13.pptx` / `.pdf` | Teacher-facing explanation of the script mismatch and corrected experiment plan |
| `results/factindic_checkpoint_for_maam_2026-11-13.pdf` | Two-page supervisor brief with workflow, results, model rationale, and limits |
| `docs/final_submission/FactIndic_Research_Paper_Final_2026-11-18.docx` / `.pdf` | Final student paper with completed metrics and limitations |
| `docs/final_submission/FactIndic_Final_Presentation_Final_2026-11-18.pptx` | Final teacher-facing presentation with project architecture and results |

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
