"""Message related commands."""

from __future__ import annotations

import click

from elsterctl.shared.cli_context import get_effective_transfer_mode


@click.group()
def message() -> None:
    """Communication with German tax offices."""


@message.command("send")
@click.pass_context
def send_message(ctx: click.Context) -> None:
    """Send a message placeholder command."""
    click.echo(f"Effective transfer mode: {get_effective_transfer_mode(ctx)}")
    raise click.ClickException("Not implemented yet.")


@message.command("fetch-inbox")
@click.option(
    "--limit",
    type=click.IntRange(1, 500),
    default=50,
    show_default=True,
    help="Maximum number of inbox messages to fetch.",
)
@click.option(
    "--unread-only",
    is_flag=True,
    help="Fetch only unread inbox messages.",
)
@click.pass_context
def fetch_inbox(ctx: click.Context, limit: int, unread_only: bool) -> None:
    """Fetch messages from the ELSTER inbox."""
    click.echo(f"Effective transfer mode: {get_effective_transfer_mode(ctx)}")
    _ = (limit, unread_only)
    raise click.ClickException("Not implemented yet.")
