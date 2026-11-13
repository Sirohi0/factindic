# Assistant-only prompt comparison

This is a descriptive aggregation of preliminary assistant source-check labels. It is not human-verified factuality data, a calibrated factuality score, or evidence that a prompt is more factually accurate. The assistant review was not blinded to prompt arm.

Seven paired Hindi/synthetic-p100 article IDs were excluded symmetrically after generation-quality checks; the retained sample has 23 paired IDs and 30 authentic MUTANT examples.

| Condition | n per arm | Standard labeled supported | Factuality-aware labeled supported | Difference |
|---|---:|---:|---:|---:|
| Hindi | 23 | 16 (69.6%) | 18 (78.3%) | +2 (+8.7 points) |
| Synthetic P100 | 23 | 14 (60.9%) | 17 (73.9%) | +3 (+13.0 points) |
| Authentic Mutant | 30 | 19 (63.3%) | 23 (76.7%) | +4 (+13.3 points) |
| **All conditions** | **76** | **49 (64.5%)** | **58 (76.3%)** | **+9 (+11.8 points)** |

## Paired label movement

Severity order for this descriptive tally: supported < minor_error < major_error < unverifiable.

| Condition | Aware arm improved | Aware arm worsened | Same label |
|---|---:|---:|---:|
| Hindi (n=23) | 4 | 2 | 17 |
| Synthetic P100 (n=23) | 6 | 3 | 14 |
| Authentic Mutant (n=30) | 9 | 5 | 16 |
| **All (n=76)** | **19** | **10** | **47** |

## Limitations

- These values count assistant screening labels only. Do not call them factuality accuracy or human factuality results.
- The assistant saw the prompt-arm labels while reviewing, so judgments were not blinded.
- The sample is small, quality-filtered, and excludes seven paired IDs with generation failures.
- Human worksheet fields remain blank; this script does not fill or replace them.
