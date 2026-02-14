"""Helpers for reading global CLI context values."""

from __future__ import annotations

import click


def resolve_transfer_mode(transfer_mode: str | None, test_transfer_mode: bool) -> str:
    """Resolve effective transfer mode.

    Precedence:
    1) explicit --transfer-mode value
    2) --test-transfer-mode flag
    3) default production mode
    """
    if transfer_mode is not None:
        return transfer_mode
    return "test" if test_transfer_mode else "prod"


def get_effective_transfer_mode(ctx: click.Context) -> str:
    """Return the globally resolved transfer mode from click context."""
    if ctx.obj is None:
        return "prod"
    mode = ctx.obj.get("transfer_mode", "prod")
    return str(mode)
