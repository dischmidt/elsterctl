"""Python-facing ERiC client façade."""

from __future__ import annotations

from elsterctl.infrastructure.eric.bindings import EricBoundSymbols, configure_base_signatures
from elsterctl.infrastructure.eric.loader import load_eric_library


class EricClient:
    """High-level client wrapping the ERiC C API."""

    def __init__(self) -> None:
        self._lib = load_eric_library()
        self._symbols: EricBoundSymbols = configure_base_signatures(self._lib)

    def initialize(self, *args: object) -> int:
        """Initialize ERiC runtime and return ERiC result code."""
        return int(self._symbols.initialize(*args))

    def process(self, *args: object) -> int:
        """Trigger ERiC processing and return ERiC result code."""
        return int(self._symbols.process(*args))

    def shutdown(self, *args: object) -> int:
        """Shutdown ERiC runtime and return ERiC result code."""
        return int(self._symbols.shutdown(*args))

