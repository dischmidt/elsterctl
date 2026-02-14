"""Root command and shell integration for elsterctl."""

from __future__ import annotations

import click
from click_shell import shell

from elsterctl.cli.address import address
from elsterctl.cli.auth import auth
from elsterctl.cli.config import config
from elsterctl.cli.message import message
from elsterctl.cli.transfer import transfer
from elsterctl.cli.vat import vat


@shell(prompt="elsterctl> ", intro="elsterctl interactive shell")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Command-line interface for ELSTER workflows."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


cli.add_command(message)
cli.add_command(address)
cli.add_command(vat)
cli.add_command(transfer)
cli.add_command(auth)
cli.add_command(config)


def main() -> None:
    """Run the CLI."""
    cli(obj={})
