"""Basic CLI smoke tests."""

from click.testing import CliRunner

from elsterctl.cli.root import cli


def test_root_help_displays_resource_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "message" in result.output
    assert "address" in result.output
    assert "vat" in result.output
    assert "transfer" in result.output
    assert "auth" in result.output
    assert "config" in result.output
