"""Tests for ERiC symbol resolution and typing."""

import ctypes

import pytest

from elsterctl.infrastructure.eric.bindings import configure_base_signatures
from elsterctl.infrastructure.eric.errors import EricSymbolResolutionError


class _FakeFunction:
    def __init__(self, return_code: int = 0) -> None:
        self.restype = None
        self._return_code = return_code

    def __call__(self, *args: object) -> int:
        _ = args
        return self._return_code


class _GermanNameLib:
    EricInitialisiere = _FakeFunction(return_code=11)
    EricBearbeiteVorgang = _FakeFunction(return_code=12)
    EricBeende = _FakeFunction(return_code=13)


class _EnglishNameLib:
    ericapi_initialize = _FakeFunction(return_code=21)
    ericapi_process = _FakeFunction(return_code=22)
    ericapi_cleanup = _FakeFunction(return_code=23)


def test_configure_base_signatures_resolves_german_symbol_names() -> None:
    symbols = configure_base_signatures(_GermanNameLib())

    assert symbols.initialize() == 11
    assert symbols.process() == 12
    assert symbols.shutdown() == 13
    assert symbols.initialize.restype is ctypes.c_int
    assert symbols.process.restype is ctypes.c_int
    assert symbols.shutdown.restype is ctypes.c_int


def test_configure_base_signatures_resolves_english_symbol_names() -> None:
    symbols = configure_base_signatures(_EnglishNameLib())

    assert symbols.initialize() == 21
    assert symbols.process() == 22
    assert symbols.shutdown() == 23


def test_configure_base_signatures_raises_when_symbol_missing() -> None:
    class _IncompleteLib:
        ericapi_initialize = _FakeFunction()

    with pytest.raises(EricSymbolResolutionError):
        configure_base_signatures(_IncompleteLib())
