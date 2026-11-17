# FactIndic final Hinglish run — 17 November 2026

## Decision

The teacher approved using any dataset. GupShup access has not been granted: the form page confirms submission only. To avoid waiting on gated access, the final pilot uses the public `suyash2739/News_Hinglish_English` dataset, pinned to revision `22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359` in the Colab notebook.

The dataset contains English news article text paired with Romanized Hinglish versions. The dataset card describes it as a translation dataset; its Hinglish side is machine-generated and curated. It has no gold summaries. The project will not treat the full English parallel article as a reference summary and will not calculate ROUGE.

## Final pilot design

- 30 fixed news items, sampled with seed 42 after an automatic script and blank-row audit.
- Same Hinglish sources passed to Qwen3 1.7B and Qwen3 4B.
- Each model uses a standard summarization prompt and a factuality-aware prompt, for 120 summaries total.
- Greedy generation; models load sequentially in a Colab GPU runtime; outputs checkpoint privately in Google Drive.
- A blinded private worksheet asks one human annotator to label factual support against each Hinglish source. The parallel English article is offered only as a reading aid.
- Paired error-rate differences use the same source IDs and bootstrap confidence intervals. Results are exploratory and single-annotator.

## Current status

- The final-run Colab notebook has been prepared at `factindic_final_open_hinglish_colab.ipynb`.
- Notebook JSON and Python code cells were checked for validity and syntax.
- No final generation has been run yet. The old Devanagari pilot is preserved as prior exploratory work and is not the corrected Roman-script result.
- No source dataset or generated row-level content is committed to GitHub.

## Remaining steps

1. In Colab, open the final notebook and select a GPU runtime.
2. Run through the dataset preview and inspect the eight selected Hinglish examples. Confirm they match the intended Roman-script style, then set `SAMPLE_LANGUAGE_CHECKED = True`.
3. Run the final generation cell. If the quality gate reports diagnostic-only, rerun the generation cell; invalid checkpoint rows are retried.
4. Complete the 120-row blinded factuality sheet against the sources. Do not fill labels automatically or mark all outputs supported without checking.
5. Upload the completed sheet to the notebook for unblinding and paired analysis.
6. Update the project report, teacher slides, and frontend with the final measured results and the dataset limitations.

## Limits to report

- This is a 30-source pilot, not a broad benchmark.
- Both models are from the Qwen3 family; it tests parameter scale, not architecture differences.
- The Hinglish inputs are machine-generated and curated translations of English news text, not naturally authored Hinglish.
- The corpus has no reference summaries, so this run evaluates factuality only and reports no ROUGE.
- Factuality findings require completed, source-grounded human labels. Automatic quality gates do not establish factual support.
