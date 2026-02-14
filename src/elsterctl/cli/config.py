"""Configuration commands."""

import click


@click.group()
def config() -> None:
    """Local configuration management."""


@config.command("show")
def show_config() -> None:
    """Show config placeholder command."""
    raise click.ClickException("Not implemented yet.")
