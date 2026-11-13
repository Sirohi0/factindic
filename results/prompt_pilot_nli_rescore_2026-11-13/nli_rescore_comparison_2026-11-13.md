# Clean-source NLI re-score audit — 13 November 2026

## Verification

- Colab output: `factindic_nli_screening_20261113T125601Z.zip`; archive SHA-256: `ae18c8f9ce9a905f61557d091d632485a5b058bfa05bd257952b46ae05e3126b`.
- Input ZIP SHA-256 recorded by Colab matches the locally prepared cleaned-input package: `True`.
- 152/152 rows match the cleaned candidate on condition, ID, prompt arm, source display, and generated summary.
- The blank human worksheet is byte-identical to the prepared worksheet; filled factuality labels: 0.
- Source replacement markers: 0; prediction replacement markers: 0; NLI hypothesis truncations: 0; all 152 rows have scores.
- 76 matched document pairs: 23 Hindi, 23 synthetic p100, and 30 authentic MUTANT.
- Device/model: Tesla T4 / `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`.

## Comparison to the 12 November NLI run

The 28 affected source-display rows now have clean display text. Across all 152 rows, every NLI probability and all chunk/token indices are numerically identical to the previous run. The stored best-source-chunk text differs in 28 rows because the terminal replacement marker was removed. Thus the prior marker did not change the NLI outputs in this run.

The paired descriptive results are also unchanged:

| Condition | Matched n | Mean aware-minus-standard entailment | Median difference | Aware higher / lower / tie | Mean contradiction difference |
|---|---:|---:|---:|---:|---:|
| authentic_mutant | 30 | +0.092044 | +0.000103 | 19 / 11 / 0 | -0.013354 |
| hindi | 23 | -0.035326 | -0.000219 | 10 / 13 / 0 | +0.041860 |
| synthetic_p100 | 23 | -0.002536 | -0.000487 | 10 / 13 / 0 | -0.043569 |

## Interpretation limits

These are automated NLI screening signals, not calibrated factuality scores or human factuality labels. Entailment medians remain near 1.0, so score saturation limits prompt comparisons. The results do not establish a prompt winner. Human annotation remains unstarted.
