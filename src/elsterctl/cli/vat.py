"""VAT declaration commands."""

from __future__ import annotations

import click

from elsterctl.shared.cli_context import get_effective_transfer_mode


@click.group()
def vat() -> None:
    """VAT filings."""


@vat.command("submit-advance")
@click.pass_context
def submit_advance(ctx: click.Context) -> None:
    """Submit VAT advance return placeholder command."""
    click.echo(f"Effective transfer mode: {get_effective_transfer_mode(ctx)}")
    raise click.ClickException("Not implemented yet.")


@vat.command("submit-annual")
@click.pass_context
def submit_annual(ctx: click.Context) -> None:
    """Submit VAT annual return placeholder command."""
    click.echo(f"Effective transfer mode: {get_effective_transfer_mode(ctx)}")
    raise click.ClickException("Not implemented yet.")
