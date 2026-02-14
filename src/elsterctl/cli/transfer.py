"""Transfer tracking commands."""

import click


@click.group()
def transfer() -> None:
    """Submission tracking and receipts."""


@transfer.command("status")
def transfer_status() -> None:
    """Transfer status placeholder command."""
    raise click.ClickException("Not implemented yet.")
