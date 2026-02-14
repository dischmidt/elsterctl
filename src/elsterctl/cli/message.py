"""Message related commands."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import click

from elsterctl.application.message_send import MessageSendRequest, MessageSendService
from elsterctl.infrastructure.eric.errors import EricError
from elsterctl.shared.cli_context import get_effective_transfer_mode


@click.group()
def message() -> None:
    """Communication with German tax offices."""


@message.command("create-template")
@click.option(
        "--output",
        "output_path",
        type=click.Path(dir_okay=False, path_type=Path),
        required=True,
        help="Path where the generated XML template should be written.",
)
@click.option(
        "--hersteller-id",
    required=False,
    envvar="ELSTER_HERSTELLER_ID",
        help="Your registered ELSTER manufacturer ID.",
)
@click.option(
        "--daten-lieferant",
        default="elsterctl",
        show_default=True,
        help="Value for TransferHeader/DatenLieferant.",
)
@click.option(
        "--subject",
        default="Test message",
        show_default=True,
        help="Message subject placeholder.",
)
@click.option(
        "--body",
        default="This is a template message body.",
        show_default=True,
        help="Message body placeholder.",
)
@click.option(
        "--testmerker",
        default="700000004",
        show_default=True,
        help="Test marker for ELSTER test runs.",
)
@click.pass_context
def create_template(
        ctx: click.Context,
        output_path: Path,
        hersteller_id: str | None,
        daten_lieferant: str,
        subject: str,
        body: str,
        testmerker: str,
) -> None:
        """Create a starter XML file for `message send`."""
        effective_hersteller_id = hersteller_id
        if effective_hersteller_id is None:
            root_obj = ctx.find_root().obj or {}
            global_hersteller_id = root_obj.get("hersteller_id")
            if global_hersteller_id:
                effective_hersteller_id = str(global_hersteller_id)

        if not effective_hersteller_id:
            raise click.ClickException(
                "Missing Hersteller-ID. Provide --hersteller-id or set ELSTER_HERSTELLER_ID."
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        xml = dedent(
                f"""\
                <?xml version="1.0" encoding="UTF-8"?>
                <Elster xmlns="http://www.elster.de/elsterxml/schema/v11">
                    <TransferHeader version="11">
                        <Verfahren>ElsterAnmeldung</Verfahren>
                        <DatenArt>sonstige_nachricht</DatenArt>
                        <Vorgang>send-Auth</Vorgang>
                        <Testmerker>{testmerker}</Testmerker>
                        <HerstellerID>{effective_hersteller_id}</HerstellerID>
                        <DatenLieferant>{daten_lieferant}</DatenLieferant>
                    </TransferHeader>
                    <DatenTeil>
                        <Nutzdatenblock>
                            <NutzdatenHeader version="11">
                                <NutzdatenTicket>0000000000000000000000000000000</NutzdatenTicket>
                            </NutzdatenHeader>
                            <Nutzdaten>
                                <Nachricht>
                                    <Betreff>{subject}</Betreff>
                                    <Text>{body}</Text>
                                </Nachricht>
                            </Nutzdaten>
                        </Nutzdatenblock>
                    </DatenTeil>
                </Elster>
                """
        )

        output_path.write_text(xml, encoding="utf-8")
        click.echo(f"Template written: {output_path}")


@message.command("send")
@click.option(
    "--xml",
    "xml_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to the ERiC transfer XML (e.g. Sonstige Nachricht payload).",
)
@click.option(
    "--certificate",
    "certificate_path",
    type=click.Path(dir_okay=False, path_type=Path),
    envvar="ELSTER_DEFAULT_CERTIFICATE",
    required=False,
    help="Path to the ELSTER certificate file (pfx/p12).",
)
@click.option(
    "--pin-env",
    default="ELSTER_CERT_PIN",
    show_default=True,
    help="Environment variable name holding the certificate PIN.",
)
@click.option(
    "--data-type-version",
    envvar="ELSTER_DEFAULT_DATA_TYPE_VERSION",
    default="TH11",
    show_default=True,
    help="ERiC data type version to submit (e.g. TH11).",
)
@click.option(
    "--validate/--no-validate",
    "validate_before_send",
    default=True,
    show_default=True,
    help="Run ERiC validation before submission.",
)
@click.pass_context
def send_message(
    ctx: click.Context,
    xml_path: Path,
    certificate_path: Path | None,
    pin_env: str,
    data_type_version: str,
    validate_before_send: bool,
) -> None:
    """Send a message XML via ERiC."""
    transfer_mode = get_effective_transfer_mode(ctx)
    click.echo(f"Effective transfer mode: {transfer_mode}")

    effective_certificate_path = certificate_path
    if effective_certificate_path is None:
        root_obj = ctx.find_root().obj or {}
        global_certificate_path = root_obj.get("certificate_path")
        if global_certificate_path:
            effective_certificate_path = Path(str(global_certificate_path))

    if effective_certificate_path is None:
        raise click.ClickException(
            "Missing certificate path. Provide --certificate either globally or for message send."
        )

    service = MessageSendService()

    request = MessageSendRequest(
        xml_path=xml_path,
        certificate_path=effective_certificate_path,
        pin_env_var=pin_env,
        data_type_version=data_type_version,
        transfer_mode=transfer_mode,
        validate_before_send=validate_before_send,
    )

    try:
        result = service.send(request)
    except (ValueError, EricError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"ERiC result code: {result.result_code}")
    if result.transfer_ticket:
        click.echo(f"Transfer ticket: {result.transfer_ticket}")
    click.echo("Message submission completed.")


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
