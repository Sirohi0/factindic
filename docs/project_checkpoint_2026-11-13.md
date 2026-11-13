# FactIndic development checkpoint — 13 November 2026

## Current position

The baseline experiments, controlled prompt pilot, assistant-only screening, clean-source NLI re-score, and MUTANT file-level provenance audit are complete. The project has a verified interim AI-only report and teacher-facing deck. Human factuality annotation has not been completed, so factuality-performance claims remain out of scope.

## Completed ladder

1. **Hindi baseline:** 500 XL-Sum Hindi test articles summarized with the pinned mT5 multilingual XLSum checkpoint; metrics and truncation records saved.
2. **Synthetic code-mix baseline:** p100 run on the same 500 article IDs; paired ROUGE evaluated against the same Hindi references. The p100 ROUGE-1/2/L F1 differences were −1.71/−1.55/−1.38 points, with paired bootstrap intervals reported.
3. **Authentic code-mix data:** MUTANT candidate mapping completed. 47/50 candidate passages match one upstream file; 3 remain ambiguous. In the 30-example prompt pilot, 28 map uniquely and 2 remain ambiguous.
4. **Prompt pilot:** 152 summaries from 76 matched documents, with standard and factuality-aware prompts. Seven Hindi/synthetic pairs were excluded symmetrically after generation-quality failures.
5. **Assistant/NLI screening:** 107 supported, 19 minor-error, and 26 major-error assistant flags. NLI medians are near 1.0, paired results vary by condition, and neither automated method establishes a prompt winner.
6. **Source-display audit:** 28 terminal replacement markers in the initial source display were removed in a separate clean copy. The clean-source NLI re-score has no markers or hypothesis truncations; all NLI probability values and chunk/token indices match the earlier run.
7. **Software and reporting:** 38 local unit tests pass. The integrated interim report, updated AI-only summary, clean-source audit, and revised 7-slide teacher deck are saved in the project.

## What remains

- If a human factuality result is required, a person must review all 152 summaries against their sources in the blinded workbook. Do not copy assistant or NLI labels into human fields.
- Only one annotator is currently available; report the single-annotator limitation and do not claim inter-annotator agreement.
- After labels are complete, unblind, compute per-condition and paired prompt comparisons, classify error types, and revise the report/deck.
- If annotation is not feasible, present the project as an exploratory AI-only checkpoint and make no human-validated factuality claim.

The 45-row assistant attention queue can help prioritize human review, but it does not replace reviewing the complete sample.

## Current files

- Integrated report: `results/factindic_interim_project_report_2026-11-13.md`
- Supervisor briefing PDF: `results/factindic_checkpoint_for_maam_2026-11-13.pdf`
- Prompt-pilot AI-only summary: `results/ai_only_prompt_pilot_summary_2026-11-13.md`
- Paired baseline comparison: `results/paired_baseline_comparison.md`
- Clean-source NLI audit: `results/prompt_pilot_nli_rescore_2026-11-13/nli_rescore_comparison_2026-11-13.md`
- MUTANT provenance audit: `results/mutant_source_provenance_audit_2026-11-13.md`
- Assistant attention queue: `results/prompt_pilot_review_candidate_2026-11-09/assistant_review_attention_queue_2026-11-13.csv`
- Teacher deck: `FactIndic_Progress_Checkpoint_2026-11-13_NLI_rescored.pptx`
