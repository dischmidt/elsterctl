"""Tests for ERiC error types."""

from elsterctl.infrastructure.eric.errors import EricProcessingError


def test_eric_processing_error_str_includes_result_code() -> None:
    error = EricProcessingError("ERiC processing failed: Detailed text", 610001226)

    assert str(error) == "ERiC processing failed: Detailed text (result_code=610001226)"
