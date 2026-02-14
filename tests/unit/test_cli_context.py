"""Tests for shared CLI context helpers."""

import click

from elsterctl.shared.cli_context import get_effective_transfer_mode, resolve_transfer_mode


def test_get_effective_transfer_mode_defaults_to_prod_when_context_has_no_object() -> None:
    ctx = click.Context(click.Command("dummy"))

    assert get_effective_transfer_mode(ctx) == "prod"


def test_get_effective_transfer_mode_reads_mode_from_context_object() -> None:
    ctx = click.Context(click.Command("dummy"), obj={"transfer_mode": "test"})

    assert get_effective_transfer_mode(ctx) == "test"


def test_resolve_transfer_mode_defaults_to_prod() -> None:
    assert resolve_transfer_mode(None, False) == "prod"


def test_resolve_transfer_mode_flag_enables_test_mode() -> None:
    assert resolve_transfer_mode(None, True) == "test"


def test_resolve_transfer_mode_parameter_has_precedence_over_flag() -> None:
    assert resolve_transfer_mode("prod", True) == "prod"
    assert resolve_transfer_mode("test", False) == "test"
