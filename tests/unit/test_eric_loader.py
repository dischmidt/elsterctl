"""ERiC loader tests."""

import pytest

from elsterctl.infrastructure.eric.errors import EricLibraryLoadError
from elsterctl.infrastructure.eric.loader import load_eric_library


def test_load_eric_library_requires_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ELSTER_ERIC_LIB", raising=False)

    with pytest.raises(EricLibraryLoadError):
        load_eric_library()
