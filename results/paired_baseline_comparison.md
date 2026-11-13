# Paired baseline comparison: Hindi vs synthetic p100

**Purpose.** Compare the existing mT5 summaries on the same 500 XL-Sum Hindi test articles, before and after synthetic p100 code-mixing. This is a lexical-overlap comparison, not a factuality evaluation.

**Method.** Matched each Hindi and synthetic p100 prediction by article ID. Scored both predictions against the same original Hindi reference using the project's Hindi-safe ROUGE implementation. For each metric, computed the per-article p100-minus-Hindi F1 difference and a 5,000-resample paired bootstrap 95% percentile interval (random seed 42).

| Metric | Hindi F1 | Synthetic p100 F1 vs same Hindi reference | Paired change (p100 − Hindi) | 95% bootstrap interval |
|---|---:|---:|---:|---:|
| ROUGE-1 | 37.24 | 35.53 | −1.71 points | [−2.47, −0.96] |
| ROUGE-2 | 16.79 | 15.24 | −1.55 points | [−2.28, −0.84] |
| ROUGE-L | 31.20 | 29.82 | −1.38 points | [−2.07, −0.69] |

Both conditions use the same 500 article IDs. Truncation status matches for 491/500 pairs; 364 Hindi sources and 355 synthetic p100 sources were marked truncated. The perturbation can change token counts, so the nine truncation-status mismatches should be disclosed.

**Interpretation.** The p100 summaries have lower ROUGE overlap against the original Hindi references in this paired sample. This supports a modest lexical-overlap drop under the synthetic perturbation, but does not establish a factuality drop or predict behavior on authentic Hinglish. ROUGE is not a factuality metric; human factuality annotation remains necessary.

**Reproduction inputs:** `results/baseline_hindi_test_n500_seed42/predictions.jsonl` and `results/baseline_codemixed_hindi_test_n500_seed42_p100/predictions.jsonl`. Scores use `reference_hi` from the synthetic p100 records for both conditions.
