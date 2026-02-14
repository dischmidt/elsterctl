"""Address update commands."""

import click


@click.group()
def address() -> None:
    """Taxpayer address updates."""


@address.command("update")
def update_address() -> None:
    """Update address placeholder command."""
    raise click.ClickException("Not implemented yet.")
