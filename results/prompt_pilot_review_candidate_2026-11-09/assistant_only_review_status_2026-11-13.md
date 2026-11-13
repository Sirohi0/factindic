# Assistant-only review status — 13 November 2026

No human factuality review has been completed, so no human label was entered. The existing unblinded assistant screening is preserved as assistant-only evidence.

## Existing assistant screening

| Condition | Prompt arm | n | Supported flags | Minor-error flags | Major-error flags |
|---|---|---:|---:|---:|---:|
| hindi | standard | 23 | 16 | 2 | 5 |
| hindi | factuality_aware | 23 | 18 | 1 | 4 |
| synthetic_p100 | standard | 23 | 14 | 2 | 7 |
| synthetic_p100 | factuality_aware | 23 | 17 | 2 | 4 |
| authentic_mutant | standard | 30 | 19 | 8 | 3 |
| authentic_mutant | factuality_aware | 30 | 23 | 4 | 3 |
| **All** | **Both arms** | **152** | **107** | **19** | **26** |

The 45 minor/major flags form an attention queue, not confirmed errors. The assistant review was not blinded to prompt arm and is not a substitute for human factuality annotation.

## Files

- `assistant_verification_all_152_source_display_cleaned_2026-11-13.csv`: all 152 existing assistant assessments with the cleaned display source; every human annotation field remains blank.
- `assistant_review_attention_queue_2026-11-13.csv`: the 45 rows with minor/major assistant flags, marked `human_review_status=pending`; no human labels were filled.

The source display cleanup removes only trailing replacement markers from token-capped display text. It does not change generated summaries or existing assistant labels.
