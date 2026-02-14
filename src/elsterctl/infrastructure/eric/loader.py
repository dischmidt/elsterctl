"""Shared library loader for ERiC native dependencies."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path

from elsterctl.infrastructure.eric.errors import EricLibraryLoadError


def load_eric_library() -> ctypes.CDLL:
    """Load the ERiC shared library from ELSTER_ERiC_LIB.

    The environment variable is intentionally explicit to keep startup
    deterministic across local setups, CI, and deployment images.
    """
    library_path = os.getenv("ELSTER_ERIC_LIB")
    if not library_path:
        raise EricLibraryLoadError("Environment variable ELSTER_ERIC_LIB is not set.")

    candidate = Path(library_path)
    if not candidate.exists():
        raise EricLibraryLoadError(f"ERiC library not found at: {candidate}")

    try:
        return ctypes.CDLL(str(candidate))
    except OSError as exc:
        raise EricLibraryLoadError(f"Failed to load ERiC library: {candidate}") from exc
