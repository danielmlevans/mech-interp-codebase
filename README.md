# mech-interp-codebase

A personal-fluency mech-interp project: residual streams, SAE features, and
attribution graphs over **Gemma-2-2B**, in three runnable notebooks.

The point of this repo is fluency, not a library — I want to read a
mech-interp paper and form a grounded opinion because I've driven the same
tooling end-to-end, not just summarised the prose.

## What's in here

Three numbered notebooks, each self-contained and runnable top-to-bottom:

| Notebook | What it does |
| --- | --- |
| [`00_setup_smoke_test`](notebooks/00_setup_smoke_test.ipynb) | Verify the env: load Gemma-2-2B via TransformerLens, run a forward pass, sanity-check shapes. |
| [`01_residual_stream`](notebooks/01_residual_stream.ipynb) | Extract and visualise layer-by-layer residual-stream activations on contrast prompt pairs. |
| [`02_sae_features`](notebooks/02_sae_features.ipynb) | Browse pre-trained Gemma Scope SAE features on a chosen task domain; pull autointerp labels from Neuronpedia. |
| [`03_attribution`](notebooks/03_attribution.ipynb) | Produce a circuit-tracer attribution graph on a non-trivial prompt with the active feature nodes annotated. |

Each notebook checkpoints its intermediate artefacts to `data/`, so you can
inspect a downstream stage without re-running the upstream forward passes.

## Stack

- **Model:** [Gemma-2-2B](https://huggingface.co/google/gemma-2-2b) (Gemma Scope SAE coverage is densest here). Llama-3.2-1B is the fallback for circuit-tracer if attribution graphs get unwieldy.
- [**TransformerLens**](https://github.com/TransformerLensOrg/TransformerLens) — hooks, activation caching, attention patching.
- [**SAELens**](https://github.com/jbloomAus/SAELens) — load and inspect pre-trained SAEs.
- [**Gemma Scope**](https://huggingface.co/google/gemma-scope) — Google's open SAE suite over Gemma-2-2B / 9B.
- [**circuit-tracer**](https://github.com/safety-research/circuit-tracer) — attribution graphs.
- [**Neuronpedia**](https://neuronpedia.org) — feature dashboards and autointerp labels (used via API).

Python 3.11+, managed with [uv](https://docs.astral.sh/uv/). Runs on local
CPU for 2B-param models; Colab T4 fallback if memory is tight.

## Quickstart

```bash
uv sync                       # creates .venv, installs from uv.lock
uv run jupyter lab notebooks/ # or point VS Code / Cursor at .venv/bin/python
```

`uv` will fetch the right Python interpreter automatically on first sync
(version pinned in `.python-version`). If you hit a CUDA / wheel mismatch,
check `pyproject.toml` for inline install notes.

## Repository layout

```
notebooks/         # 00–03, runnable top-to-bottom
src/mech_interp/   # shared model-loading so notebooks don't double-load Gemma into RAM
data/              # cached activations, SAE outputs, attribution artefacts (gitignored)
pyproject.toml     # source of truth for pins; uv.lock is the reproducible resolution
REFERENCES.md      # curated list of related repos (deps, tutorials, paper companions)
```

The `src/mech_interp/` package is intentionally minimal — one shared
model-load code path. This is a personal-fluency project; premature
abstraction is the failure mode.

## Reproducibility

Direct pins in `pyproject.toml`, full transitive resolution in `uv.lock`
(committed). When upgrading a dependency, record the reason in the commit
message — "bumped to fix X" beats a silent version bump for future-me.

Sources for the direct pins:

- transformer_lens: <https://pypi.org/project/transformer-lens/>
- sae_lens: <https://pypi.org/project/sae-lens/> · [CHANGELOG](https://github.com/jbloomAus/SAELens/blob/main/CHANGELOG.md)
- gemma_scope: <https://huggingface.co/google/gemma-scope-2b-pt-res> · [paper](https://arxiv.org/abs/2408.05147)
- circuit_tracer: <https://github.com/safety-research/circuit-tracer>
- neuronpedia: <https://docs.neuronpedia.org/features> · <https://www.neuronpedia.org/gemma-scope>

## Related work

See [`REFERENCES.md`](REFERENCES.md) for a curated list of GitHub repos with
overlapping scope (deps, methodology mirrors, tutorials, reference
implementations, paper companions). Machine-readable companion at
[`references.json`](references.json).
