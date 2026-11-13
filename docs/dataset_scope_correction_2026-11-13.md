# Dataset scope correction — Roman-script Hinglish

**Status:** the current code-mixed experiments do not match the intended Roman-script Hinglish target. Keep the old outputs for audit and describe them as preliminary script-mixed experiments. Do not use the current human-review workbook as the main Hinglish factuality evaluation.

## Intended input style

The project should focus on Hindi-English Hinglish written in Latin/Roman characters: Hindi words transliterated into the English alphabet, with English words and phrases mixed in. The example that motivated this correction is “Hindi is a Bharatiya bhaasha, it is ek aisi bhasha jo poore india me boli jaati hai.”

This is a script and data-distribution requirement. Devanagari Hindi sentences containing English tokens are a different written style and are not a substitute for the target examples.

## Audit of the existing pilot

The 76 unique source documents in `results/prompt_pilot_review_candidate_2026-11-09/generations_source_display_cleaned_2026-11-13.csv` were inspected by script. All 76 contain Devanagari characters; none is Roman-script Hinglish. The current condition counts are:

| Existing condition | Sources | Mean Devanagari characters | Mean Latin letters |
|---|---:|---:|---:|
| Hindi | 23 | 425.9 | 0.0 |
| Synthetic p100 | 23 | 416.7 | 46.6 |
| MUTANT sample | 30 | 401.2 | 43.6 |

Therefore, the existing pilot can support only exploratory observations about its Devanagari-based data. It cannot support a result about the intended Roman-script Hinglish setting. The 500-item Hindi and synthetic baseline results also remain valid for their original Hindi-script task; they are not Hinglish baselines.

## Recommended replacement data

Use the **Hinglish-dialogue-to-English-summary (h2e) split of GupShup** as the primary task candidate. The paper describes Romanized Hindi-English conversations and human-annotated English and Hi-En summaries. It reports 6,831 conversations. The conversations were manually translated from SAMSum by bilingual annotators, so this is human-produced Romanized Hinglish but not a corpus of organically collected chat conversations. Report that limitation explicitly.

The authors' repository says to request access through their form and identifies `h2e` source and target files for Hinglish-to-English summarization. The form requires a person to provide contact and affiliation information, agree to cite the paper, and agree not to redistribute the data. Do not upload the restricted corpus to this public repository. Keep it in the user's private Colab/Drive workspace and publish only derived aggregate results and code.

**Access request:** <https://docs.google.com/forms/d/1zvUk7WcldVF3RCoHdWzQPzPprtSJClrnHoIOYbzaJEI/viewform?ts=61381ec0&edit_requested=true>

## Corrected experimental plan

1. Obtain GupShup access and inspect the `h2e` train/validation/test files. Use `scripts/audit_romanized_parallel.py` to check line alignment and script characteristics, then manually inspect its private sample before retaining the official test split.
2. The ready Colab notebook samples 30 fixed sources from the official test split, verifies source/reference row alignment, records truncation per tokenizer, and creates a private run manifest. The first pilot contains 120 outputs (30 sources × 2 models × 2 prompts); it is exploratory.
3. Compare Qwen3-4B and Gemma 3 4B IT on identical sources and decoding settings. Both model cards describe multilingual support; their similar size makes a constrained Colab comparison practical. Qwen3's model card lists 100+ languages, and Gemma 3 lists 140+; these claims do not guarantee Hinglish performance. Gemma access requires accepting Google's Hugging Face terms. See the [Qwen3-4B model card](https://huggingface.co/Qwen/Qwen3-4B) and [Gemma 3 4B IT model card](https://huggingface.co/google/gemma-3-4b-it).
4. For each model, use paired standard and factuality-aware instructions with greedy decoding. Heavy generation runs in Colab, not on the Mac.
5. Review the 120 generated summaries in a blinded, private sheet. Judge against the source, not the reference. Do not annotate the existing 152-summary sheet as the target Hinglish result.
6. Compare English reference-based ROUGE separately from source-based human factuality. Report the single-annotator limit and exploratory sample size; no NLI score is treated as a factuality result.
7. The ready notebook exports a separate aggregate-only archive without sources, references, row IDs, or generations. Keep the full run and annotation data private; update the report, slides, and dashboard only after the corrected run and labels are complete.

## Natural-data limitation and backup

L3Cube-HingCorpus is a large real-world Roman-script Hindi-English corpus, but the cited resource is for language modeling and downstream NLP tasks rather than a source-summary dataset. It has no ready-made summary references. It could be an auxiliary no-reference factuality set only if the project creates and transparently annotates summaries; it is not a drop-in replacement for GupShup h2e.

## Materials to hold

- `results/human_annotation_pack_2026-11-12/FactIndic_blinded_annotation.xlsx` — leave blank; it was prepared from the mismatched 152-summary pilot.
- Existing Colab prompt-pilot outputs, NLI screens, and prior reports — preserve as earlier exploratory work; do not present as evidence on Roman-script Hinglish.
- Prior Hindi and synthetic p100 baseline outputs — preserve under their original Hindi-script task labels.
