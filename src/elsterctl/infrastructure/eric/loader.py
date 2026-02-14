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

    if os.name == "posix" and "darwin" in os.sys.platform:
        _prepare_macos_runtime(candidate)

    try:
        return ctypes.CDLL(str(candidate), mode=ctypes.RTLD_GLOBAL)
    except OSError as exc:
        raise EricLibraryLoadError(f"Failed to load ERiC library: {candidate}") from exc


def _prepare_macos_runtime(main_library: Path) -> None:
    lib_dir = main_library.parent

    existing_paths = os.getenv("DYLD_LIBRARY_PATH", "")
    updated_paths = [str(lib_dir)]
    if existing_paths:
        updated_paths.append(existing_paths)
    os.environ["DYLD_LIBRARY_PATH"] = ":".join(updated_paths)

    for dependency in sorted(lib_dir.glob("liberic*.dylib")):
        if dependency == main_library:
            continue
        try:
            ctypes.CDLL(str(dependency), mode=ctypes.RTLD_GLOBAL)
        except OSError:
            continue
