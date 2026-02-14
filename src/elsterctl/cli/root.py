"""Root command and shell integration for elsterctl."""

from __future__ import annotations

import json
import os

import click
from click_shell import shell

from elsterctl.cli.address import address
from elsterctl.cli.auth import auth
from elsterctl.cli.config import config
from elsterctl.cli.message import message
from elsterctl.cli.transfer import transfer
from elsterctl.cli.vat import vat
from elsterctl.shared.cli_context import resolve_transfer_mode


@shell(prompt="elsterctl> ", intro="elsterctl interactive shell")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option(
    "--transfer-mode",
    type=click.Choice(["prod", "test"], case_sensitive=False),
    default=None,
    help="Force transfer mode globally: prod or test.",
)
@click.option(
    "--test-transfer-mode",
    is_flag=True,
    help="Enable test-enabled transfer mode globally unless --transfer-mode is set.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    verbose: bool,
    transfer_mode: str | None,
    test_transfer_mode: bool,
) -> None:
    """Command-line interface for ELSTER workflows."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["transfer_mode"] = resolve_transfer_mode(transfer_mode, test_transfer_mode)
    ctx.obj["test_transfer_mode"] = ctx.obj["transfer_mode"] == "test"


@cli.command("show-config")
@click.option("--json", "as_json", is_flag=True, help="Print configuration as JSON.")
@click.pass_context
def show_config(ctx: click.Context, as_json: bool) -> None:
    """Show effective global runtime configuration."""
    config_data = {
        "verbose": ctx.obj.get("verbose", False),
        "transfer_mode": ctx.obj.get("transfer_mode", "prod"),
        "test_transfer_mode": ctx.obj.get("test_transfer_mode", False),
        "eric_lib": os.getenv("ELSTER_ERIC_LIB", ""),
    }

    if as_json:
        click.echo(json.dumps(config_data, indent=2, sort_keys=True))
        return

    click.echo(f"verbose={config_data['verbose']}")
    click.echo(f"transfer_mode={config_data['transfer_mode']}")
    click.echo(f"test_transfer_mode={config_data['test_transfer_mode']}")
    click.echo(f"eric_lib={config_data['eric_lib']}")


cli.add_command(message)
cli.add_command(address)
cli.add_command(vat)
cli.add_command(transfer)
cli.add_command(auth)
cli.add_command(config)


def main() -> None:
    """Run the CLI."""
    cli(obj={})
