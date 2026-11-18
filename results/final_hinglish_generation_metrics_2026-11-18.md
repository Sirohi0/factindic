# Final Hinglish generation metrics

The final Colab run generated 120 summaries from 30 fixed Roman-script Hinglish news sources. This aggregate comes from the user-provided private review ZIP. It contains no article text, summaries, row-level labels, or blinded identifiers.

| Model | Prompt | Outputs | Mean summary words | Mean compression | Corpus compression | Mean generation seconds | Median generation seconds | Source truncations |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen3 1.7B | Standard | 30 | 53.77 | 0.7702 | 0.7696 | 4.540 | 3.297 | 0 |
| Qwen3 1.7B | Factuality-aware | 30 | 46.70 | 0.6752 | 0.6684 | 3.032 | 2.848 | 0 |
| Qwen3 4B | Standard | 30 | 54.10 | 0.7829 | 0.7743 | 4.750 | 4.493 | 0 |
| Qwen3 4B | Factuality-aware | 30 | 49.30 | 0.7101 | 0.7056 | 4.126 | 4.109 | 0 |

Across all 120 outputs, mean summary length was 50.97 words; mean source length was 69.87 words; mean per-document compression was 0.7346; corpus compression was 0.7295. The quality audit recorded 0 token-cap hits, 0 empty outputs, 0 replacement-character rows, and 0 truncated sources. Two summaries lacked terminal punctuation and should be visually inspected before quoting examples.

Generation time is descriptive of this Colab Tesla T4 run. Compression and length do not measure factuality. The corpus has no gold summaries, so ROUGE is not applicable. The AI-assisted factuality labels remain unvalidated by a human annotator.
