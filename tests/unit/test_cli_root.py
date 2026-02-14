"""Basic CLI smoke tests."""

import json

from click.testing import CliRunner

from elsterctl.cli.root import cli
from elsterctl.shared.cli_context import resolve_transfer_mode


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
    assert "show-config" in result.output


def test_root_help_displays_global_transfer_options() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "--transfer-mode" in result.output
    assert "--test-transfer-mode" in result.output


def test_resolve_transfer_mode_defaults_to_prod() -> None:
    assert resolve_transfer_mode(None, False) == "prod"


def test_resolve_transfer_mode_flag_enables_test_mode() -> None:
    assert resolve_transfer_mode(None, True) == "test"


def test_resolve_transfer_mode_parameter_has_precedence_over_flag() -> None:
    assert resolve_transfer_mode("prod", True) == "prod"
    assert resolve_transfer_mode("test", False) == "test"


def test_show_config_prints_effective_runtime_values() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--verbose", "--transfer-mode", "test", "show-config"],
        env={"ELSTER_ERIC_LIB": "/tmp/libericapi.dylib"},
    )

    assert result.exit_code == 0
    assert "verbose=True" in result.output
    assert "transfer_mode=test" in result.output
    assert "test_transfer_mode=True" in result.output
    assert "force_test_mode=" in result.output
    assert "hersteller_id=" in result.output
    assert "eric_lib=/tmp/libericapi.dylib" in result.output


def test_show_config_json_outputs_structured_configuration() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--transfer-mode", "test", "show-config", "--json"],
        env={"ELSTER_ERIC_LIB": "/tmp/libericapi.dylib"},
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["transfer_mode"] == "test"
    assert payload["test_transfer_mode"] is True
    assert payload["force_test_mode"] == ""
    assert payload["hersteller_id"] == ""
    assert payload["verbose"] is False
    assert payload["eric_lib"] == "/tmp/libericapi.dylib"


def test_force_test_mode_blocks_prod_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--transfer-mode", "prod", "show-config"],
        env={"ELSTERCTL_FORCE_TEST_MODE": "1"},
    )

    assert result.exit_code == 1
    assert "Production mode is blocked" in result.output


def test_force_test_mode_allows_test_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--transfer-mode", "test", "show-config"],
        env={"ELSTERCTL_FORCE_TEST_MODE": "1"},
    )

    assert result.exit_code == 0
    assert "transfer_mode=test" in result.output


def test_transfer_mode_defaults_from_env_when_option_omitted() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["show-config"],
        env={"ELSTER_DEFAULT_TRANSFER_MODE": "test"},
    )

    assert result.exit_code == 0
    assert "transfer_mode=test" in result.output
    assert "test_transfer_mode=True" in result.output


def test_transfer_mode_option_overrides_env_default() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--transfer-mode", "prod", "show-config"],
        env={"ELSTER_DEFAULT_TRANSFER_MODE": "test"},
    )

    assert result.exit_code == 0
    assert "transfer_mode=prod" in result.output
    assert "test_transfer_mode=False" in result.output
