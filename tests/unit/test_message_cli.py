"""Tests for message command group."""

from pathlib import Path

from click.testing import CliRunner

from elsterctl.application.message_send import MessageSendResult
from elsterctl.cli.root import cli


def test_message_help_lists_fetch_inbox_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["message", "--help"])

    assert result.exit_code == 0
    assert "fetch-inbox" in result.output
    assert "create-template" in result.output


def test_message_help_accepts_global_certificate_option() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "test",
            "--certificate",
            "certs/test-soft-pse.pfx",
            "message",
            "--help",
        ],
    )

    assert result.exit_code == 0


def test_message_help_accepts_global_hersteller_id_option() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "test",
            "--hersteller-id",
            "74931",
            "message",
            "send",
            "--help",
        ],
    )

    assert result.exit_code == 0


def test_message_send_uses_test_transfer_mode_from_global_flag(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>")
    cert_path = tmp_path / "cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = (self, request)
        return MessageSendResult(0, "ticket-123", "", "")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--test-transfer-mode",
            "message",
            "send",
            "--xml",
            str(xml_path),
            "--certificate",
            str(cert_path),
        ],
    )

    assert result.exit_code == 0
    assert "Effective transfer mode: test" in result.output


def test_message_send_uses_parameter_precedence_over_test_flag(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>")
    cert_path = tmp_path / "cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = (self, request)
        return MessageSendResult(0, "ticket-123", "", "")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "prod",
            "--test-transfer-mode",
            "message",
            "send",
            "--xml",
            str(xml_path),
            "--certificate",
            str(cert_path),
        ],
    )

    assert result.exit_code == 0
    assert "Effective transfer mode: prod" in result.output


def test_message_send_returns_click_exception_for_service_errors(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader></TransferHeader>")
    cert_path = tmp_path / "cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = (self, request)
        raise ValueError("invalid request")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "message",
            "send",
            "--xml",
            str(xml_path),
            "--certificate",
            str(cert_path),
        ],
    )

    assert result.exit_code == 1
    assert "invalid request" in result.output


def test_message_send_uses_global_certificate_option(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>")
    cert_path = tmp_path / "global-cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = self
        assert request.certificate_path == cert_path
        return MessageSendResult(0, "ticket-123", "", "")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "test",
            "--certificate",
            str(cert_path),
            "message",
            "send",
            "--xml",
            str(xml_path),
        ],
    )

    assert result.exit_code == 0
    assert "Message submission completed." in result.output


def test_message_send_uses_default_certificate_from_env(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>")
    cert_path = tmp_path / "env-cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = self
        assert request.certificate_path == cert_path
        return MessageSendResult(0, "ticket-123", "", "")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "test",
            "message",
            "send",
            "--xml",
            str(xml_path),
        ],
        env={"ELSTER_DEFAULT_CERTIFICATE": str(cert_path)},
    )

    assert result.exit_code == 0
    assert "Message submission completed." in result.output


def test_message_send_uses_default_data_type_version_from_env(
    monkeypatch,
    tmp_path: Path,
) -> None:
    xml_path = tmp_path / "message.xml"
    xml_path.write_text("<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>")
    cert_path = tmp_path / "cert.pfx"
    cert_path.write_text("dummy")

    def _fake_send(self, request):
        _ = self
        assert request.data_type_version == "ESt_2020"
        return MessageSendResult(0, "ticket-123", "", "")

    monkeypatch.setattr("elsterctl.application.message_send.MessageSendService.send", _fake_send)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "test",
            "--certificate",
            str(cert_path),
            "message",
            "send",
            "--xml",
            str(xml_path),
        ],
        env={"ELSTER_DEFAULT_DATA_TYPE_VERSION": "ESt_2020"},
    )

    assert result.exit_code == 0
    assert "Message submission completed." in result.output


def test_message_create_template_writes_xml_file(tmp_path: Path) -> None:
    runner = CliRunner()
    output_path = tmp_path / "message-template.xml"

    result = runner.invoke(
        cli,
        [
            "message",
            "create-template",
            "--output",
            str(output_path),
            "--hersteller-id",
            "12345",
            "--subject",
            "Hello",
            "--body",
            "World",
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")
    assert "<HerstellerID>12345</HerstellerID>" in content
    assert "<Betreff>Hello</Betreff>" in content
    assert "<Text>World</Text>" in content


def test_message_create_template_reads_hersteller_id_from_env(tmp_path: Path) -> None:
    runner = CliRunner()
    output_path = tmp_path / "message-template-env.xml"

    result = runner.invoke(
        cli,
        [
            "message",
            "create-template",
            "--output",
            str(output_path),
        ],
        env={"ELSTER_HERSTELLER_ID": "54321"},
    )

    assert result.exit_code == 0
    content = output_path.read_text(encoding="utf-8")
    assert "<HerstellerID>54321</HerstellerID>" in content
