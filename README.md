# Mech-interp codebase

> Scaffolded from `vault/01-projects/code/mech-interp-codebase.md` — keep the spec as the source of truth.
> If `vault/01-projects/code/mech-interp-codebase.md` and this README drift, the spec wins; edit it there
> and re-render the relevant sections here by hand.

## Outcome

By 2026-06-30, I can pull residual-stream activations from Gemma-2-2B, browse pre-trained Gemma Scope SAE features, and render a circuit-tracer attribution graph on a chosen prompt — from a single repo of three runnable notebooks. Specifically: (a) `notebooks/01_residual_stream.ipynb` extracts and visualises layer-by-layer activations on at least one contrast prompt pair; (b) `notebooks/02_sae_features.ipynb` identifies and characterises at least three Gemma Scope features that fire on a chosen task domain, with autointerp labels pulled from Neuronpedia; (c) `notebooks/03_attribution.ipynb` produces a circuit-tracer attribution graph on a single non-trivial prompt with the active feature nodes annotated. The deliverable is fluency — me being able to read a mech-interp paper and form an opinion grounded in having driven the same tooling, not just summarised the prose.

## Architecture

- **Repo layout:** `notebooks/` + `data/` + `pyproject.toml` (managed by [uv](https://docs.astral.sh/uv/)), with a minimal `src/mech_interp/` package for shared model-loading so notebooks do not double-load Gemma-2-2B into RAM. No CLI. Personal-fluency project — the package is intentionally one file; premature abstraction is the failure mode.
- **Entry points:** three numbered notebooks, each self-contained and runnable top-to-bottom. Designed to be read like a worked exercise, not a library.
- **Model substrate:** Gemma-2-2B as the residual-stream + SAE host (Gemma Scope coverage is densest here). Llama-3.2-1B as fallback for circuit-tracer if Gemma-2-2B attribution graphs are unwieldy.
- **External deps:** TransformerLens (hooks), SAELens (SAE loading), HuggingFace `transformers` (model loading), Neuronpedia API (feature labels), circuit-tracer (attribution).
- **Data flow:** prompts (hand-curated) → forward pass with hooks → cached activations → SAE encoder → feature activations → attribution graph. Each notebook checkpoints its intermediate artefacts to `data/` so reruns aren't required to inspect downstream stages.
- **Runtime:** local CPU for 2B-param models; Colab T4 fallback if memory is tight. No production-grade infra concerns — this is a single-user notebook project.

## Stack

- Language: python (3.11+)
- Kind: script (notebooks)
- Repo: (create on GitHub at start of Phase 1; mirror URL into `repo:` frontmatter)
- Key dependencies:
  - [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) — residual-stream hooks, activation caching, attention patching
  - [SAELens](https://github.com/jbloomAus/SAELens) — load and inspect pre-trained SAEs
  - [Gemma Scope](https://huggingface.co/google/gemma-scope) — Google's open SAE suite over Gemma-2-2B / 9B
  - [circuit-tracer](https://github.com/safety-research/circuit-tracer) — attribution graphs (Anthropic-adjacent)
  - [Neuronpedia](https://neuronpedia.org) — feature dashboards + autointerp labels (used via API, not committed as a dep)

**Layout idiom:** notebooks/ + data/ + pyproject.toml per the spec, with one src/ module (`mech_interp`) added to share the model-load code path across notebooks. No CLI. Personal-fluency project: premature abstraction is the failure mode.

## Setup

This is a [uv](https://docs.astral.sh/uv/) local project. `pyproject.toml`
is the source of truth for pins; `uv.lock` is the reproducible resolution.

```bash
uv sync                       # creates .venv, installs from uv.lock
uv run jupyter lab notebooks/ # or point VS Code at .venv/bin/python
```

Python version is pinned in `.python-version` (3.12). `uv` will fetch a
matching interpreter automatically on first sync.

If you hit a CUDA / wheel mismatch, check `pyproject.toml` for inline
install notes carried over from the research pass.

## Reproducibility

This repo was scaffolded with pinned versions from a Perplexity research
pass. The pins live in `pyproject.toml`; `uv.lock` captures the full
transitive resolution and should be committed. Sources for the direct pins:

- transformer_lens: https://pypi.org/project/transformer-lens/
- sae_lens: https://pypi.org/project/sae-lens/
- sae_lens: https://github.com/jbloomAus/SAELens/blob/main/CHANGELOG.md
- gemma_scope: https://huggingface.co/google/gemma-scope-2b-pt-res
- gemma_scope: https://arxiv.org/abs/2408.05147
- circuit_tracer: https://github.com/safety-research/circuit-tracer
- neuronpedia: https://docs.neuronpedia.org/features
- neuronpedia: https://www.neuronpedia.org/gemma-scope
- neuronpedia: https://pypi.org/project/neuronpedia/

When upgrading a dependency, record the reason in the commit message —
"bumped to fix X" beats a silent version bump for future-you.

## Related repositories

See [`REFERENCES.md`](REFERENCES.md) — a curated list of GitHub repos with
overlapping scope (deps, methodology mirrors, tutorials, reference
implementations, paper companions). Machine-readable companion at
[`references.json`](references.json). To add a repo, use
`append_reference.py` in the scaffolding-code-projects skill — never
hand-edit the rendered Markdown.

## Project metadata

- **Language:** python
- **Kind:** script
- **Slug:** mech-interp-codebase
- **Spec:** `vault/01-projects/code/mech-interp-codebase.md`
