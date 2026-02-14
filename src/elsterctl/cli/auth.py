"""Authentication commands."""

import click


@click.group()
def auth() -> None:
    """Authentication and certificate handling."""


@auth.command("login")
def login() -> None:
    """Login placeholder command."""
    raise click.ClickException("Not implemented yet.")
