# Final Roman-script Hinglish pilot: AI-assisted screening

**Run:** `final_hinglish_news_835e0687b9b9`
**Status:** generation complete; AI-assisted factuality screening complete; human validation not started.

## Design and dataset

The pilot used 30 fixed items from the public `suyash2739/News_Hinglish_English` corpus, pinned to revision `22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359`. It generated 120 summaries: Qwen3-1.7B and Qwen3-4B, each with standard and factuality-aware prompts, using the same source items. Generation ran greedily on a Colab Tesla T4.

The dataset pairs English news articles with Romanized Hinglish translations. Its Hinglish side is machine-generated and curated, so it does not represent naturally authored Hinglish. There are no gold summaries. ROUGE was therefore not calculated.

## Generation quality audit

| Check | Result |
|---|---:|
| Outputs | 120 / 120 |
| Token-cap hits | 0 |
| Empty outputs | 0 |
| Replacement characters | 0 |
| Truncated sources | 0 |
| Outputs without terminal punctuation | 2 |

Mechanical checks establish export readiness only; they do not establish factuality.

## AI-assisted source comparison

The 120 blinded source-summary pairs were compared by one AI reviewer against the model-visible Hinglish source. The paired English article was a reading aid only. Labels were 19 supported, 27 minor errors, and 74 major errors (0 cannot-determine). These are provisional AI judgments, not human annotation or factuality gold labels. They must not be represented as human-verified results.

| Model | Prompt | Supported | Minor | Major | AI-assessed error rate |
|---|---|---:|---:|---:|---:|
| Qwen3-1.7B | Standard | 2/30 | 4 | 24 | 93.3% |
| Qwen3-1.7B | Factuality-aware | 4/30 | 8 | 18 | 86.7% |
| Qwen3-4B | Standard | 6/30 | 9 | 15 | 80.0% |
| Qwen3-4B | Factuality-aware | 7/30 | 6 | 17 | 76.7% |

Paired bootstrap error-rate differences (AI labels; factuality-aware minus standard) were −6.7 percentage points for Qwen3-1.7B (95% interval −20.0 to +6.7) and −3.3 points for Qwen3-4B (−13.3 to +6.7). Both intervals include zero. These screening results do not establish a prompt winner. The AI review also found frequent number, date, entity, relation, and attribution errors; the detailed AI-labeled sheet is private and is not included in this repository.

## Current conclusion

The corrected Roman-script pilot is now executed, and the generated sample is suitable for exploratory review. The AI pass flags substantial factual drift across both models and prompt styles, but the judgments are not independently validated. There is no human factuality result, no claim of a factuality winner, and no generalization beyond this small news-domain sample.

## Remaining work

1. If the project requires factuality results, have a human annotator verify the 120 labels against the exact source text; preserve the current AI sheet as a separate screen.
2. Recompute and publish the final aggregate only from human labels if a human review is completed.
3. The teacher-facing checkpoint deck and frontend now show these results with the AI/human distinction.
4. If presenting a factuality outcome, complete human verification and publish a revised analysis; otherwise present this strictly as an AI-screened exploratory pilot.

## Reproducibility and privacy

The notebook, dataset revision, sample seed, model IDs, generation parameters, and quality audit are recorded in the private run metadata. Row-level news text, generated summaries, and individual labels are not committed to the public repository.
