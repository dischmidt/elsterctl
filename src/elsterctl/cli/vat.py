"""VAT declaration commands."""

import click


@click.group()
def vat() -> None:
    """VAT filings."""


@vat.command("submit-advance")
def submit_advance() -> None:
    """Submit VAT advance return placeholder command."""
    raise click.ClickException("Not implemented yet.")


@vat.command("submit-annual")
def submit_annual() -> None:
    """Submit VAT annual return placeholder command."""
    raise click.ClickException("Not implemented yet.")
