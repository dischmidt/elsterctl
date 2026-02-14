"""Transfer tracking commands."""

from __future__ import annotations

import click

from elsterctl.shared.cli_context import get_effective_transfer_mode


@click.group()
def transfer() -> None:
    """Submission tracking and receipts."""


@transfer.command("status")
@click.pass_context
def transfer_status(ctx: click.Context) -> None:
    """Transfer status placeholder command."""
    click.echo(f"Effective transfer mode: {get_effective_transfer_mode(ctx)}")
    raise click.ClickException("Not implemented yet.")
