# FactIndic prompt pilot — AI-only evidence summary

**Status:** exploratory screening. Human factuality labels are blank; this report does not establish factual accuracy or a winning prompt.

## Study snapshot

- 152 summaries from 76 paired source documents.
- Hindi: 23 pairs; synthetic p100: 23 pairs; authentic MUTANT: 30 pairs.
- Seven Hindi/synthetic pairs were excluded symmetrically after generation-quality failures.
- Standard and factuality-aware prompts were run on the same source within each condition.

## Automated generation and source-display checks

The retained generation candidate had zero new-token cap hits, empty summaries, or replacement characters in generated summaries. The initial visible source field had one terminal U+FFFD marker in 28 rows (14 source-condition examples). Each affected source was token-capped. A clean display copy removes only the final marker; it does not guess or add a character. The cleaned-source NLI re-score contains zero source markers and the same 152 summaries.

## Assistant-only source-check pass

The unblinded assistant review flagged 107 summaries as supported, 19 as minor errors, and 26 as major errors. Supported-label counts were 49/76 in the standard arm and 58/76 in the factuality-aware arm. The paired review marked the aware arm improved on 19 documents, worsened on 10, and unchanged on 47. These are assistant triage labels only; they are not verified error rates or human judgments. Of the 45 flagged rows, the assistant taxonomy recorded 13 relation, 13 unsupported-addition, 5 date, 5 entity, 3 attribution, 2 number, 2 polarity, and 2 other flags.

## Multilingual NLI screening

Model: `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. The mean max-entailment score was 0.8572 and the median was 0.9980, indicating ceiling saturation.

| Condition | Matched documents | Mean aware-minus-standard entailment | Median difference |
|---|---:|---:|---:|
| Authentic MUTANT | 30 | +0.0920 | +0.0001 |
| Hindi | 23 | −0.0353 | −0.0002 |
| Synthetic p100 | 23 | −0.0025 | −0.0005 |

Contradiction signals moved in different directions across conditions. The cleaned-source re-score was compared row by row with the 12 November run: every probability and chunk/token index was unchanged. Only the stored best-source-chunk string changed in the 28 cleaned rows. The median scores remain near 1.0, so score saturation limits interpretation. No prompt winner is supported.

## Limits and next step

Assistant review was not blinded. NLI is not calibrated for factuality. Human factuality labels remain blank. If factuality claims are required, annotate all 152 rows using the blinded worksheet, keep the key separate, and report the single-annotator limitation. The 45-row assistant attention queue can prioritize review but does not replace labeling the full sample. If annotation is not feasible, present results as an AI-only exploratory checkpoint.

## Audit trail

- Assistant-only comparison: `results/assistant_only_prompt_comparison_2026-11-09.md`
- Clean-source NLI audit: `results/prompt_pilot_nli_rescore_2026-11-13/nli_rescore_comparison_2026-11-13.md`
- Clean-source display and row audit: `results/prompt_pilot_review_candidate_2026-11-09/source_display_integrity_audit_2026-11-13.md`
- MUTANT source mapping: `results/mutant_source_provenance_audit_2026-11-13.md`
