"""Tests for message command group."""

from click.testing import CliRunner

from elsterctl.cli.root import cli


def test_message_help_lists_fetch_inbox_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["message", "--help"])

    assert result.exit_code == 0
    assert "fetch-inbox" in result.output


def test_message_send_uses_test_transfer_mode_from_global_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--test-transfer-mode", "message", "send"])

    assert result.exit_code == 1
    assert "Effective transfer mode: test" in result.output


def test_message_send_uses_parameter_precedence_over_test_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--transfer-mode", "prod", "--test-transfer-mode", "message", "send"],
    )

    assert result.exit_code == 1
    assert "Effective transfer mode: prod" in result.output
