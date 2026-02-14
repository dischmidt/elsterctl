"""Custom exceptions for ERiC integration."""


class EricError(Exception):
    """Base exception for ERiC related failures."""


class EricLibraryLoadError(EricError):
    """Raised when ERiC shared libraries cannot be loaded."""


class EricSymbolResolutionError(EricError):
    """Raised when required ERiC API symbols cannot be resolved."""

