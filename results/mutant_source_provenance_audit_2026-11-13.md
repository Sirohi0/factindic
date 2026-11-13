# MUTANT source-file provenance audit — 13 November 2026

## Result

The 50 local authentic-code-mixed candidates were compared with the official `LingoIITGN/MUTANT` repository snapshot `e7a454a71d4f9d1f3ebb65544868610e513d9366` (retrieved 13 November 2026).

| Match outcome | Rows |
|---|---:|
| Unique upstream file path: exact full-text match | 2 |
| Unique upstream file path: local text is an exact file prefix | 8 |
| Unique upstream file path: local text is an exact in-file span | 37 |
| Ambiguous: exact text occurs in two files | 3 |
| No exact match within the declared subset | 0 |
| **Total** | **50** |

The three ambiguous project IDs are `PM-speech_014` (files `pm-speech/94.txt` and `pm-speech/95.txt`), `PM-speech_020` and `PM-speech_023` (both match `pm-speech/258.txt` and `pm-speech/259.txt`). These rows remain explicitly ambiguous; do not select one file without additional evidence.

The 47 unique matches identify an upstream text file within the declared MUTANT subset. The local source passage matched exactly after Unicode NFC normalization and whitespace collapse. Match type distinguishes full-file equality, prefix, and unique in-file span. A prefix/span match means the local passage occurs in that official file; it does not mean the local project ID is an original MUTANT ID.

The prompt-comparison pilot uses 30 of these 50 authentic examples. The row-level manifest cross-checks those IDs against the pilot metadata: 28 of the 30 map to one file and 2 are ambiguous. The ambiguous pilot IDs are `PM-speech_014` and `PM-speech_020`; `PM-speech_023` is ambiguous in the broader 50-row candidate collection but was not selected for the prompt pilot.

## Files

- Row-level mapping with pinned file links, match class, and local text SHA-256: `mutant_source_provenance_map_2026-11-13.csv`.
- Reproducible standard-library script: `scripts/map_mutant_provenance.py` (rerun with `python3 scripts/map_mutant_provenance.py` from the project root; it checks 655 public text files, about 7.35 MB total).
- Original candidate file remains unchanged: `authentic_code_mixed_candidates.csv`.
- Dataset card and citation: [official MUTANT dataset card](https://huggingface.co/datasets/LingoIITGN/MUTANT) and [Gupta, Srivastava, and Singh (2023), Findings of EACL](https://aclanthology.org/2023.findings-eacl.56/).

## Method and limits

1. Read the public file listing for the two declared subsets at the pinned repository revision: 597 `pm-speech` files and 58 `mankibaat` files (655 total).
2. Compared each local candidate text with all files in its declared subset. Matching normalized strings with NFC Unicode normalization and collapsed whitespace; no semantic/fuzzy match was accepted.
3. A unique path is a file-level source match. Three passages are present in two files and cannot be disambiguated from the local sample alone.
4. The MUTANT files provide stable dataset-file URLs, but they do not supply original event/news URLs for the underlying political speech or radio/news item. Do not claim recovery of those original publisher URLs.
5. The official dataset card declares CC BY 4.0 and requests citation of the MUTANT paper. Preserve attribution when redistributing derived text.

## Reproducibility

- Dataset: `LingoIITGN/MUTANT`
- Immutable repository revision: `e7a454a71d4f9d1f3ebb65544868610e513d9366`
- Subset directories checked: `pm-speech/`, `mankibaat/`
- Mapping output: `results/mutant_source_provenance_map_2026-11-13.csv`
