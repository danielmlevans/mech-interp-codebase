# References for Mech-interp codebase

> Generated from `references.json` — **do not hand-edit this file**.
> To add or update an entry, run:
>
> ```bash
> python3 .claude/skills/scaffolding-code-projects/scripts/append_reference.py \
>   --slug mech-interp-codebase \
>   --url <github-url> \
>   --category <category> \
>   --summary "<one-line summary>" \
>   [--relevance-notes "<why this repo is here>"] \
>   [--linked-phase <N>]
> ```
>
> **Categories**
>
> | Category | Meaning |
> |---|---|
> | `dependency` | A library this project imports directly. |
> | `methodology` | A repo implementing a comparable workflow / pipeline. |
> | `tutorial` | A walkthrough, course, or worked-example notebook series. |
> | `reference-impl` | A specific technique implemented end-to-end. |
> | `benchmark` | An eval suite or shared benchmark. |
> | `inspiration` | Similar scope, different stack — for cross-pollination. |
> | `companion` | The code companion to a paper this project leans on. |

## Direct dependencies

### [TransformerLensOrg/TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) `dependency`

Residual-stream hooks + ActivationCache library for decoder-only transformers; the primary mech-interp instrument.

**Why here:** Used in every Phase 1 notebook via HookedTransformer + run_with_cache. Originally by Neel Nanda, now maintained by Bryce Meyer. — **Linked phase:** 1


### [jbloomAus/SAELens](https://github.com/jbloomAus/SAELens) `dependency`

Loader and analysis library for pre-trained sparse autoencoders (incl. Gemma Scope).

**Why here:** Phase 2 entry point for SAE feature browsing; SAE.from_pretrained() pulls Gemma Scope weights. — **Linked phase:** 2


### [safety-research/circuit-tracer](https://github.com/safety-research/circuit-tracer) `dependency`

Open-source attribution-graph engine released by Anthropic / Decode Research in 2025; produces input-specific causal graphs over interpretable features.

**Why here:** Phase 3 entry point. Supports Gemma-2 (2B) and Llama-3.2 (1B). Backbone of Ameisen et al. 2025 and Lindsey et al. 2025 (Biology of a Large Language Model). — **Linked phase:** 3


## Methodology — comparable workflows

### [ndif-team/nnsight](https://github.com/ndif-team/nnsight) `methodology`

Hook + intervention library from David Bau's group (Northeastern NDIF) for activation patching and remote execution on production-scale models.

**Why here:** Alternative to TransformerLens that scales past local memory. Backend option inside circuit-tracer. Worth comparing when Gemma-2-2B starts to feel small.


### [stanfordnlp/pyvene](https://github.com/stanfordnlp/pyvene) `methodology`

Causal-abstraction and distributed-alignment-search (DAS) intervention library from Stanford NLP.

**Why here:** The reference toolkit for the causal-abstraction line of mech-interp work (Geiger et al. 2023). Natural companion to the RAVEL benchmark.


## Reference implementations

### [saprmarks/feature-circuits](https://github.com/saprmarks/feature-circuits) `reference-impl`

Implementation of Sparse Feature Circuits (Marks et al. 2024) — SAE features as nodes in an automatically discovered causal graph, with feature-level editing.

**Why here:** Worked example of replacing neurons with SAE features as circuit nodes. Echoes the Phase 2 → Phase 3 transition this codebase is rehearsing. — **Linked phase:** 3


### [callummcdougall/sae_vis](https://github.com/callummcdougall/sae_vis) `reference-impl`

Sparse autoencoder feature visualisation tool (top-activating prompts, logit attribution, distribution plots).

**Why here:** Drop-in for the Phase 2 "one-paragraph human gloss per feature" task once Gemma Scope features are identified. — **Linked phase:** 2


## Tutorials and walkthroughs

### [callummcdougall/ARENA_3.0](https://github.com/callummcdougall/ARENA_3.0) `tutorial`

ARENA mech-interp curriculum (Chapter 1 covers transformers from scratch, probes, SAEs, IOI, superposition).

**Why here:** The structured curriculum this codebase shadow-follows. Phase 1 maps to ARENA Day 2-3; Phase 2 to the SAE chapter.


## Paper companions

### [openai/sparse_autoencoder](https://github.com/openai/sparse_autoencoder) `companion`

Companion code to Gao et al. (2024), "Scaling and Evaluating Sparse Autoencoders" — the top-k SAE that became the architectural default after mid-2024.

**Why here:** Reference architecture for the top-k variant whose theoretical motivation the Phase 2 notebook will lean on. Useful for comparing against Gemma Scope's L1-style SAEs. — **Linked phase:** 2


---

_Last updated: 2026-05-16T00:16:57Z_
_Schema: `references.json` v1.0_
