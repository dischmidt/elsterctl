"""ctypes declarations for selected ERiC C API symbols.

The concrete ERiC symbol names differ across wrapper generations. This
module resolves a small baseline set of lifecycle symbols with fallback
names (German and English-style naming).
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from typing import Any

from elsterctl.infrastructure.eric.errors import EricSymbolResolutionError


class EricHandle(ctypes.Structure):
    """Opaque ERiC handle placeholder type."""


@dataclass(frozen=True)
class EricBoundSymbols:
    """Resolved and typed ERiC function references."""

    initialize: Any
    process: Any
    shutdown: Any


def _resolve_symbol(eric_lib: ctypes.CDLL, candidates: tuple[str, ...], logical_name: str) -> Any:
    for symbol_name in candidates:
        try:
            return getattr(eric_lib, symbol_name)
        except AttributeError:
            continue

    raise EricSymbolResolutionError(
        f"Could not resolve ERiC symbol for '{logical_name}'. Tried: {', '.join(candidates)}"
    )


def configure_base_signatures(eric_lib: ctypes.CDLL) -> EricBoundSymbols:
    """Configure baseline ctypes signatures for lifecycle operations.

    Baseline symbols for first integration stage:
    - Initialize ERiC runtime
    - Process a transfer workflow
    - Shutdown ERiC runtime

    `argtypes` are intentionally kept open in this stage because exact
    prototypes depend on the shipped Release 43 header set.
    """
    initialize = _resolve_symbol(
        eric_lib,
        candidates=("EricInitialisiere", "ericapi_initialize"),
        logical_name="initialize",
    )
    process = _resolve_symbol(
        eric_lib,
        candidates=("EricBearbeiteVorgang", "ericapi_process"),
        logical_name="process",
    )
    shutdown = _resolve_symbol(
        eric_lib,
        candidates=("EricBeende", "ericapi_cleanup"),
        logical_name="shutdown",
    )

    initialize.restype = ctypes.c_int
    process.restype = ctypes.c_int
    shutdown.restype = ctypes.c_int

    return EricBoundSymbols(
        initialize=initialize,
        process=process,
        shutdown=shutdown,
    )
