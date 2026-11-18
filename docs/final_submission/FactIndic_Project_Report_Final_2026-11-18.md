# FactIndic — Final Project Report

**Course:** CSET 346 – Natural Language Processing (Bennett University)  
**Student:** Sanchit Sirohi (Enrollment ID: `S24CSEU0393`)  
**Instructor:** Dr. Geetanjali Singh  
**Date:** 18 November 2026  
**Repository:** [github.com/Sirohi0/factindic](https://github.com/Sirohi0/factindic)

---

## 1. Executive Summary

FactIndic investigates **factuality-aware abstractive summarization for Hindi and Roman-script Hinglish** (Hindi written in Latin letters mixed with English). Lexical-overlap metrics such as ROUGE do not detect whether a fluent summary alters a date, number, entity, negation, or attribution. FactIndic separates **reference-based overlap evaluation** (where gold summaries exist) from **source-grounded factuality review**.

The completed project delivers:
1. **Paired Hindi vs. Synthetic Code-Mixed Baseline (500 articles):** `csebuetnlp/mT5_multilingual_XLSum` evaluated on 500 XL-Sum Hindi test articles (seed 42) and a synthetic `p100` code-mixed perturbation against the same Hindi references.
2. **Corrected Roman-Script Hinglish Pilot (30 sources × 4 conditions = 120 summaries):** Qwen3 1.7B and Qwen3 4B with standard vs. factuality-aware prompts on `suyash2739/News_Hinglish_English` (pinned revision `22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359`), audited for generation quality, length/compression, latency, and AI-assisted source comparison.
3. **Live Interactive Colab Evaluation Demo:** Single-input Roman-script Hinglish summarization and claim-evidence verification on a Colab T4 GPU (`factindic_interactive_evaluation_colab.ipynb`), using pure greedy decoding, numeric/date/name consistency guards, verbatim source-quote checking, and a secondary cross-lingual NLI signal (`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`).
4. **Native macOS Results Viewer:** A SwiftUI viewer (`macos/FactIndicApp/`) presenting baseline and pilot results without running local model inference.
5. **Engineering Verification:** **49 local unit tests passing** (`pytest`), cleanly compiled macOS viewer, and reproducible metadata tracking.

**Core Limitation:** Human factuality annotation was intentionally skipped for this version. All 120-summary screening labels and live interactive claim checks are **AI-assisted signals**, not human-verified factuality gold labels, and no prompt or model is claimed as a factuality winner.

---

## 2. Dataset Scope Correction

An earlier exploratory pilot (152 summaries across 76 matched documents) compared standard vs. factuality-aware prompts on XL-Sum Hindi, synthetic `p100`, and MUTANT passages, followed by assistant triage and `mDeBERTa-v3-base-mnli-xnli` NLI re-scoring. A script audit on 13 November 2026 confirmed that all 76 unique sources in that pilot contained Devanagari script rather than Roman-script Hinglish. Those earlier Devanagari and NLI runs are preserved solely as historical/exploratory background (`results/prompt_pilot_nli_rescore_2026-11-13/`).

Because gated GupShup `h2e` access remained pending, the final pilot used the public `suyash2739/News_Hinglish_English` parallel corpus (pinned to revision `22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359`). Its Hinglish side is machine-generated and curated from English news, and it contains no gold summaries—so ROUGE is omitted for the final Hinglish pilot.

---

## 3. System Architecture

- **Offline / Reproducible Python Pipeline (`src/factindic/`, `scripts/`):** Pinned mT5 and XL-Sum loading, resumable inference, Hindi-safe ROUGE tokenization, deterministic number/date/novel-token checks, and paired bootstrap confidence intervals (5,000 resamples, seed 42).
- **Colab T4 GPU Experiments (`factindic_final_open_hinglish_colab.ipynb`):** Runs Qwen3 1.7B and Qwen3 4B sequentially on a Tesla T4 (greedy decoding, 1,024-token source budget) and exports generation quality and aggregate metrics.
- **Live Interactive Colab Demo (`factindic_interactive_evaluation_colab.ipynb`):** Accepts pasted Roman-script Hinglish (2,048-token cap), generates a concise English summary via pure greedy decoding (no `repetition_penalty` or `no_repeat_ngram_size`, which previously caused ±1 digit and entity distortions), retries once on numeric/date mismatches, applies cautious unique-date and close-name disclosures, extracts atomic claims with verbatim source-quote verification, and runs `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` as a secondary cross-lingual NLI check. Outputs with any unresolved mismatch, unverified quote, or NLI contradiction remain labeled **Draft summary — not factually verified**.
- **Native macOS Results Viewer (`macos/FactIndicApp/`):** Read-only SwiftUI application displaying baseline comparisons, pilot metrics, methods, and limitations.

---

## 4. Quantitative & Exploratory Results

### 4.1 Paired Hindi vs. Synthetic `p100` Baseline (`N = 500`, XL-Sum Test)

| Metric | Hindi F1 | Synthetic p100 F1 | Paired Change | 95% Bootstrap CI |
|---|---:|---:|---:|---:|
| ROUGE-1 | 37.24 | 35.53 | −1.71 pp | [−2.47, −0.96] |
| ROUGE-2 | 16.79 | 15.24 | −1.55 pp | [−2.28, −0.84] |
| ROUGE-L | 31.20 | 29.82 | −1.38 pp | [−2.07, −0.69] |

Input truncation (512-token cap) occurred in 364/500 Hindi articles and 355/500 `p100` articles (491/500 matched truncation status). This measures lexical overlap against Hindi references under synthetic perturbation, not factuality or natural Hinglish performance.

### 4.2 Final Roman-Script Hinglish Pilot (`N = 30` Sources × 4 Conditions = 120 Outputs)

**Mechanical Quality Audit:** 120/120 outputs generated; 0 token-cap hits, 0 empty outputs, 0 replacement characters, 0 truncated sources; 2 outputs lacked terminal punctuation.

| Model | Prompt | Supported | Minor | Major | AI Error Rate | Mean Words | Mean Doc Comp. | Corpus Comp. | Mean Sec. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3 1.7B | Standard | 2 | 4 | 24 | 93.3% | 53.77 | 0.7702 | 0.7696 | 4.540 |
| Qwen3 1.7B | Factuality-aware | 4 | 8 | 18 | 86.7% | 46.70 | 0.6752 | 0.6684 | 3.032 |
| Qwen3 4B | Standard | 6 | 9 | 15 | 80.0% | 54.10 | 0.7829 | 0.7743 | 4.750 |
| Qwen3 4B | Factuality-aware | 7 | 6 | 17 | 76.7% | 49.30 | 0.7101 | 0.7056 | 4.126 |

Paired bootstrap error-rate differences (factuality-aware minus standard) were **−6.7 pp** for Qwen3 1.7B (95% CI: −20.0 to +6.7) and **−3.3 pp** for Qwen3 4B (95% CI: −13.3 to +6.7). Both intervals include zero, so no prompt winner is established.

### 4.3 Live Interactive Colab T4 Challenge Suite

After removing `repetition_penalty=1.03` and `no_repeat_ngram_size=3`, live T4 testing across five challenge categories (single date + named entities, two dates, number-heavy transit news, explicit negation/warning, and clean no-number Hinglish) showed:
- **Exact entity & digit preservation:** Previous ±1 digit shifts (`1923`, `11/41/160/14`) and `checker_mismatch` entity mutations disappeared across Qwen3 1.7B and 4B, with `quote_found_in_model_input = True` on all extracted claims.
- **Model-size gap:** Qwen3 4B preserved all five transit figures in their exact roles and translated *"kaafi suhana tha"* accurately (*"quite pleasant"*), whereas Qwen3 1.7B misread *"12 nayi"* as *"12 November"* and inverted *"kaafi suhana tha"* to *"very hot and the air was humid"*.
- **Secondary NLI (`mDeBERTa-v3-base-mnli-xnli`) behavior:** Flagged the 1.7B weather inversion as `contradiction` (0.784), but also produced a false-positive `contradiction` (0.682–0.902) on the negation/warning passage because it was trained on Devanagari Hindi/English XNLI rather than Roman-script Hinglish. Conservative fallback kept that output labeled **Draft summary — not factually verified**.

---

## 5. Limitations & Conclusion

- **Sample & Domain:** 30 machine-curated news translations do not represent informal, naturally authored Hinglish across social or conversational domains.
- **Unvalidated Signals:** Neither the 120-summary AI screen nor the secondary `mDeBERTa` NLI check substitutes for human source-grounded annotation.
- **Engineering Readiness:** All **49 local unit tests** pass, the macOS SwiftUI viewer builds, and the live Colab demo reliably surfaces uncertainty rather than masking model errors.

---

## 6. References

1. T. Hasan et al., "XL-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages," *Findings of ACL-IJCNLP*, 2021.
2. L. Xue et al., "mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer," *NAACL-HLT*, 2021.
3. W. Kryscinski et al., "Evaluating the Factual Consistency of Abstractive Text Summarization," *EMNLP*, 2020.
4. A. Gupta, A. Srivastava, and A. Singh, "MUTANT: A Multi-sentential Code-mixed Hinglish Dataset," *Findings of EACL*, 2023.
5. S. Agarwal, "News_Hinglish_English: An English–Hinglish Parallel Corpus," Hugging Face Datasets, 2024.
6. A. Yang et al., "Qwen3 Technical Report," arXiv:2505.09388, 2025.
7. C.-Y. Lin, "ROUGE: A Package for Automatic Evaluation of Summaries," *ACL Workshop*, 2004.
