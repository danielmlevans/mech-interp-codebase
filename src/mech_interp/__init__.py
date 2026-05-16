"""Shared model loaders for the notebooks.

Why this exists: each Jupyter kernel holds its own copy of the model in RAM,
and Gemma-2-2B at fp32 on MPS is ~10 GB resident (plus a transient duplicate
during TransformerLens's HF-weight rewrite). `get_model` memoises within a
kernel so re-running a notebook — or running multiple notebooks from the
same kernel via `%run` — does not re-instantiate weights.

Cross-kernel sharing is not possible at the Python level: if two VS Code
notebooks each spawn a kernel and both call `get_model`, RAM doubles. To
keep one copy resident, either run both notebooks from one kernel, or shut
the first kernel down (Command Palette → *Jupyter: Shut Down Kernel*)
before opening the next.
"""

from __future__ import annotations

import gc
from functools import lru_cache

import torch
from transformer_lens import HookedTransformer


def select_device_dtype() -> tuple[str, torch.dtype]:
    """Pick (device, dtype) appropriate for the host.

    fp16 on MPS halves weight RAM vs fp32 and is stable for Gemma-2 inference;
    bf16 on MPS has known correctness issues in TransformerLens 3.x.
    """
    if torch.cuda.is_available():
        return 'cuda', torch.bfloat16
    if torch.backends.mps.is_available():
        return 'mps', torch.float16
    return 'cpu', torch.float32


@lru_cache(maxsize=1)
def _load(name: str, device: str, dtype: torch.dtype) -> HookedTransformer:
    model = HookedTransformer.from_pretrained(name, device=device, dtype=dtype)
    model.eval()
    return model


def get_model(
    name: str = 'gemma-2-2b',
    device: str | None = None,
    dtype: torch.dtype | None = None,
) -> HookedTransformer:
    """Return a (cached) HookedTransformer. Subsequent calls in the same kernel
    return the same instance — the model is loaded at most once per process."""
    if device is None or dtype is None:
        d, t = select_device_dtype()
        device = device or d
        dtype = dtype or t
    return _load(name, device, dtype)


def unload_model() -> None:
    """Drop the cached model and reclaim RAM."""
    _load.cache_clear()
    gc.collect()
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    elif torch.cuda.is_available():
        torch.cuda.empty_cache()


__all__ = ['get_model', 'select_device_dtype', 'unload_model']
