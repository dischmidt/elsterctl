"""Message related commands."""

import click


@click.group()
def message() -> None:
    """Communication with tax authorities."""


@message.command("send")
def send_message() -> None:
    """Send a message placeholder command."""
    raise click.ClickException("Not implemented yet.")
