"""Helpers for reading global CLI context values."""

from __future__ import annotations

import os

import click


def _is_force_test_mode_enabled() -> bool:
    value = os.getenv("ELSTERCTL_FORCE_TEST_MODE", "")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def resolve_transfer_mode(transfer_mode: str | None, test_transfer_mode: bool) -> str:
    """Resolve effective transfer mode.

    Precedence:
    1) explicit --transfer-mode value
    2) --test-transfer-mode flag
    3) default production mode
    """
    if transfer_mode is not None:
        resolved_mode = transfer_mode
    else:
        resolved_mode = "test" if test_transfer_mode else "prod"

    if _is_force_test_mode_enabled() and resolved_mode != "test":
        raise ValueError(
            "Production mode is blocked because ELSTERCTL_FORCE_TEST_MODE is enabled. "
            "Use --transfer-mode test."
        )

    return resolved_mode


def get_effective_transfer_mode(ctx: click.Context) -> str:
    """Return the globally resolved transfer mode from click context."""
    if ctx.obj is None:
        return "prod"
    mode = ctx.obj.get("transfer_mode", "prod")
    return str(mode)
