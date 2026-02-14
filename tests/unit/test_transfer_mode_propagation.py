"""Tests for global transfer mode propagation across command groups."""

from click.testing import CliRunner

from elsterctl.cli.root import cli


def test_vat_submit_advance_uses_test_transfer_mode_from_global_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--test-transfer-mode", "vat", "submit-advance"])

    assert result.exit_code == 1
    assert "Effective transfer mode: test" in result.output


def test_vat_submit_annual_uses_parameter_precedence_over_test_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--transfer-mode",
            "prod",
            "--test-transfer-mode",
            "vat",
            "submit-annual",
        ],
    )

    assert result.exit_code == 1
    assert "Effective transfer mode: prod" in result.output


def test_transfer_status_uses_global_test_transfer_mode() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--test-transfer-mode", "transfer", "status"])

    assert result.exit_code == 1
    assert "Effective transfer mode: test" in result.output
