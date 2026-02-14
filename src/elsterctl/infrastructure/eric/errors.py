"""Custom exceptions for ERiC integration."""


class EricError(Exception):
    """Base exception for ERiC related failures."""


class EricLibraryLoadError(EricError):
    """Raised when ERiC shared libraries cannot be loaded."""


class EricSymbolResolutionError(EricError):
    """Raised when required ERiC API symbols cannot be resolved."""


class EricProcessingError(EricError):
    """Raised when ERiC processing returns a non-success result code."""

    def __init__(self, message: str, result_code: int) -> None:
        super().__init__(message)
        self.result_code = result_code

    def __str__(self) -> str:
        return f"{super().__str__()} (result_code={self.result_code})"


