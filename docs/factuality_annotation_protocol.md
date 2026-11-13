# FactIndic factuality annotation protocol (pilot)

## Purpose and scope

This protocol labels whether each claim in a generated summary is supported by the exact source text supplied to the summarizer. The source shown to annotators must be the model-visible source after the recorded input truncation. Keep the original full article only as optional context and record separately if it changes a judgment.

The pilot compares two prompts for the same model and the same source examples: standard summarization and factuality-aware summarization. It also includes the saved mT5 outputs as a project baseline. Do not treat ROUGE, automatic flags, or NLI output as factuality gold labels.

## Unit and labels

Annotate the whole summary, then mark claim-level errors in notes. Use one mutually exclusive summary label:

- `supported`: all checkable claims are entailed by the visible source; harmless paraphrase/compression is allowed.
- `minor_error`: a small detail is imprecise or weakly supported, but the main event/relationship remains correct.
- `major_error`: at least one material claim is contradicted, unsupported, or changes a key entity, number, date, polarity, attribution, or relation.
- `unverifiable`: the source is too incomplete/unclear to decide, or the summary contains no checkable claim.

For aggregate factuality, report supported summaries / all decidable summaries. Also report minor and major error counts separately. Do not silently count `unverifiable` as supported.

For every `minor_error` or `major_error`, record the shortest offending summary span, the relevant source evidence (or “not present”), and an error type: `entity`, `number`, `date`, `relation`, `polarity`, `attribution`, `unsupported_addition`, `omission`, `other`. Omission alone is not a factuality error unless it changes the meaning.

## Annotation workflow

1. Show source and summary together. Hide system/model arm labels during first-pass annotation where practical.
2. Judge only what the source supports; outside knowledge does not make an unsupported statement supported.
3. For truncated inputs, judge against the truncated source that the model saw. If a full source is used to diagnose truncation, note that separately.
4. Have two people independently label a shared subset (target: at least 20% of the pilot, and at least 20 examples per language/data condition if feasible). Discuss disagreements and record an adjudicated label without overwriting either original label.
5. Report agreement (raw agreement; Cohen’s kappa for two annotators if labels are sufficiently populated) and adjudication procedure. If only one human annotator is available, say so explicitly and avoid inter-annotator reliability claims.
6. Use automatic number/novelty checks and NLI scores only to prioritize review. They do not replace a human decision.

## Sampling and comparisons

For the initial presentation pilot, target 30 examples per condition: Hindi, synthetic p100 code-mix, and authentic MUTANT Hinglish. Use the same 30 article IDs for Hindi and synthetic p100 so the source condition is paired. Sample authentic examples reproducibly and balance across available subsets. Run both prompt arms on every selected source. Compare paired examples; report the sample size and uncertainty, and do not generalize the small pilot to all Hindi/Hinglish summarization.

Keep each dataset condition distinct. Synthetic p100 is a controlled perturbation of Hindi and is not authentic Hinglish. MUTANT is a corpus of naturally occurring multi-sentential code-mixed text assembled from political speeches/press releases and Hindi news sources; document the subset/source, sample IDs, transformations, and license. The local 50-row candidate file should be checked against the official MUTANT records before publication.

## Reporting

For each data condition and prompt arm, report number of summaries, supported/minor/major/unverifiable counts, supported percentage among decidable summaries, and annotation agreement. Also report ROUGE only where a suitable reference exists, summary length, compression, truncation, and latency. For Hindi and synthetic code-mix, the Hindi reference is not automatically a valid target for synthetic mixed input; label any such metric clearly. Do not call an NLI score “factuality accuracy” without human calibration and validation.
