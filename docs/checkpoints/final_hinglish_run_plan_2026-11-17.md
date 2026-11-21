# FactIndic final Hinglish run — 17 November 2026

## Decision

The teacher approved using any dataset. GupShup access has not been granted: the form page confirms submission only. To avoid waiting on gated access, the final pilot uses the public `suyash2739/News_Hinglish_English` dataset, pinned to revision `22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359` in the Colab notebook.

The dataset contains English news article text paired with Romanized Hinglish versions. The dataset card describes it as a translation dataset; its Hinglish side is machine-generated and curated. It has no gold summaries. The project will not treat the full English parallel article as a reference summary and will not calculate ROUGE.

## Final pilot design

- 30 fixed news items, sampled with seed 42 after an automatic script and blank-row audit.
- Same Hinglish sources passed to Qwen3 1.7B and Qwen3 4B.
- Each model uses a standard summarization prompt and a factuality-aware prompt, for 120 summaries total.
- Greedy generation; models load sequentially in a Colab GPU runtime; outputs checkpoint privately in Google Drive.
- The private worksheet was designed for a human annotator to label factual support against each Hinglish source. The parallel English article is a reading aid only. A later AI-assisted pass filled the review labels; this does not count as human annotation.
- Paired error-rate differences use the same source IDs and bootstrap confidence intervals. The available comparisons are exploratory AI screening only.

## Current status

- The final Colab run completed on a Tesla T4: 30 sources and 120 outputs across two Qwen3 sizes and two prompt styles.
- The quality gate passed: 0 cap hits, empty outputs, replacement-character rows, or truncated sources; 2 outputs lacked terminal punctuation.
- A source-grounded AI screening pass produced 19 supported, 27 minor-error, and 74 major-error labels. These are AI assessments, not human factuality labels.
- The user-provided Section 7 ZIP contains the final per-condition generation metrics. The aggregate report and CSV are in `results/final_hinglish_generation_metrics_2026-11-18.md` and `.csv`.
- The aggregate metrics show mean summaries from 46.70 to 54.10 words and mean generation time from 3.032 to 4.750 seconds per output across conditions. These are descriptive values from a Colab Tesla T4 run.
- No row-level source, summary, blinded key, or review data is committed to GitHub.

## Project status

The current exploratory version is complete: the final generation run, mechanical audit, per-condition metrics export, AI-assisted source screen, research paper, presentation, and native results viewer are aligned. Human factuality validation was explicitly skipped. A later human review would be needed only for claims about human-verified factuality; it is not a required step for presenting this version.

## Limits to report

- This is a 30-source pilot, not a broad benchmark.
- Both models are from the Qwen3 family; it tests parameter scale, not architecture differences.
- The Hinglish inputs are machine-generated and curated translations of English news text, not naturally authored Hinglish.
- The corpus has no reference summaries, so this run reports no ROUGE. The factuality comparison is AI-assisted screening, not a verified human evaluation.
- Factuality findings require completed, source-grounded human labels. Automatic quality gates do not establish factual support.
