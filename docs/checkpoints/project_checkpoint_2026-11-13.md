# FactIndic development checkpoint — 13 November 2026

## Critical scope correction — 13 November 2026

The intended code-mixed target is Roman-script Hinglish: Hindi words transliterated into Latin characters, mixed with English. A script audit of the 76 unique sources in the earlier prompt pilot found Devanagari characters in all 76 and zero Roman-script Hinglish sources. Thus, the current prompt pilot and MUTANT sample do not test the intended input style. Preserve their results as exploratory, Devanagari-based prior work; do not present them as Roman-script Hinglish evidence or annotate the existing 152-row sheet as the target evaluation. The Hindi and synthetic p100 baselines remain useful for their original Hindi-script task.

The recommended replacement is GupShup's h2e task: Romanized Hinglish conversations with English summaries. Its source paper says the conversations were manually translated from SAMSum, so it is suitable for Romanized Hinglish summarization but does not represent naturally collected chat. Dataset access is by request and carries a no-redistribution condition. The user must request access; the public repository must not contain the restricted corpus. See [dataset scope correction](dataset_scope_correction_2026-11-13.md).

## Previous experimental position

The previous-scope baseline experiments, controlled prompt pilot, assistant-only screening, clean-source NLI re-score, and MUTANT file-level provenance audit are complete. Human factuality annotation was not completed. Due to the script-style mismatch, the prior code-mixed findings are not final evidence for the intended Roman-script Hinglish task.

## Completed ladder

1. **Hindi baseline:** 500 XL-Sum Hindi test articles summarized with the pinned mT5 multilingual XLSum checkpoint; metrics and truncation records saved.
2. **Synthetic code-mix baseline:** p100 run on the same 500 article IDs; paired ROUGE evaluated against the same Hindi references. The p100 ROUGE-1/2/L F1 differences were −1.71/−1.55/−1.38 points, with paired bootstrap intervals reported.
3. **Authentic code-mix data:** MUTANT candidate mapping completed. 47/50 candidate passages match one upstream file; 3 remain ambiguous. In the 30-example prompt pilot, 28 map uniquely and 2 remain ambiguous.
4. **Prompt pilot:** 152 summaries from 76 matched documents, with standard and factuality-aware prompts. Seven Hindi/synthetic pairs were excluded symmetrically after generation-quality failures.
5. **Assistant/NLI screening:** 107 supported, 19 minor-error, and 26 major-error assistant flags. NLI medians are near 1.0, paired results vary by condition, and neither automated method establishes a prompt winner.
6. **Source-display audit:** 28 terminal replacement markers in the initial source display were removed in a separate clean copy. The clean-source NLI re-score has no markers or hypothesis truncations; all NLI probability values and chunk/token indices match the earlier run.
7. **Software and reporting:** 38 local unit tests pass. The corrected Colab notebook is prepared and syntax/mocked-workflow checked; the integrated interim report, AI-only summary, clean-source audit, and corrected 7-slide scope deck are saved in the project.

## Corrected development ladder

1. **Request GupShup access:** complete the authors' access form, including the citation and no-redistribution agreements.
2. **Audit the authorized `h2e` split:** run `scripts/audit_romanized_parallel.py` for pair alignment and script counts, manually inspect its private sample for real Hindi-English mixing, and verify split integrity and truncation. Do not use the unrelated Roman-script Gupshup chat corpus found elsewhere on the Hub.
3. **Run a paired two-model, two-prompt comparison:** same official test sources for each model and prompt arm. Heavy generation stays in Colab.
4. **Create a new blinded human factuality worksheet** for the corrected Roman-script sample. The old 152-row worksheet remains blank and is out of scope.
5. **Evaluate separately:** reference-based summary quality; blinded human factuality; NLI as an exploratory signal only.
6. **Revise the report, deck, and dashboard** to put the corrected experiment first and retain prior Hindi-script results as background.

## What remains from the previous plan

- For the corrected experiment, a person must review the newly generated summaries against their sources. Do not copy assistant or NLI labels into human fields.
- Only one annotator is currently available; report the single-annotator limitation and do not claim inter-annotator agreement.
- After labels are complete, unblind, compute per-condition and paired prompt comparisons, classify error types, and revise the report/deck.
- If annotation is not feasible, present the corrected model comparison as an exploratory AI-only checkpoint and make no human-validated factuality claim.

The 45-row assistant attention queue can help prioritize human review, but it does not replace reviewing the complete sample.

## Current files

- Integrated report: `results/factindic_interim_project_report_2026-11-13.md`
- Corrected teacher deck and brief: `FactIndic_Scope_Correction_2026-11-13.pptx` and `.pdf`
- Corrected Roman-script Colab pilot: `factindic_romanized_hinglish_colab.ipynb` (run after GupShup access and teacher data-fit confirmation)
- Previous-scope supervisor brief: `results/factindic_checkpoint_for_maam_2026-11-13.pdf` (do not present as Roman-script Hinglish evidence)
- Prompt-pilot AI-only summary: `results/ai_only_prompt_pilot_summary_2026-11-13.md`
- Paired baseline comparison: `results/paired_baseline_comparison.md`
- Clean-source NLI audit: `results/prompt_pilot_nli_rescore_2026-11-13/nli_rescore_comparison_2026-11-13.md`
- MUTANT provenance audit: `results/mutant_source_provenance_audit_2026-11-13.md`
- Assistant attention queue: `results/prompt_pilot_review_candidate_2026-11-09/assistant_review_attention_queue_2026-11-13.csv`
- Previous-scope teacher deck: `FactIndic_Progress_Checkpoint_2026-11-13_NLI_rescored.pptx` (do not present as Roman-script Hinglish evidence)
