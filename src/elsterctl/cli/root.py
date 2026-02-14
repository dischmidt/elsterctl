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
    "--certificate",
    default=None,
    help="Global certificate path used by commands that require certificate authentication.",
)
@click.option(
    "--hersteller-id",
    envvar="ELSTER_HERSTELLER_ID",
    default=None,
    help="Global ELSTER Hersteller-ID. Can also be provided via ELSTER_HERSTELLER_ID.",
)
@click.option(
    "--transfer-mode",
    type=click.Choice(["prod", "test"], case_sensitive=False),
    envvar="ELSTER_DEFAULT_TRANSFER_MODE",
    default=None,
    help="Force transfer mode globally: prod or test. Can also be set via ELSTER_DEFAULT_TRANSFER_MODE.",
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
    certificate: str | None,
    hersteller_id: str | None,
    transfer_mode: str | None,
    test_transfer_mode: bool,
) -> None:
    """Command-line interface for ELSTER workflows."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["certificate_path"] = certificate
    ctx.obj["hersteller_id"] = hersteller_id
    try:
        ctx.obj["transfer_mode"] = resolve_transfer_mode(transfer_mode, test_transfer_mode)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
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
        "force_test_mode": os.getenv("ELSTERCTL_FORCE_TEST_MODE", ""),
        "hersteller_id": ctx.obj.get("hersteller_id") or "",
        "eric_lib": os.getenv("ELSTER_ERIC_LIB", ""),
    }

    if as_json:
        click.echo(json.dumps(config_data, indent=2, sort_keys=True))
        return

    click.echo(f"verbose={config_data['verbose']}")
    click.echo(f"transfer_mode={config_data['transfer_mode']}")
    click.echo(f"test_transfer_mode={config_data['test_transfer_mode']}")
    click.echo(f"force_test_mode={config_data['force_test_mode']}")
    click.echo(f"hersteller_id={config_data['hersteller_id']}")
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
