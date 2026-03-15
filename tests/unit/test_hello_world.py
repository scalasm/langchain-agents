"""Unit tests for hello_world module."""

from typer.testing import CliRunner

from my_langchain_agents.hello_world import GREETING_MESSAGE, app, hello

runner = CliRunner()


def test_hello_prints_greeting_message(capsys: object) -> None:
    """Test that hello() prints the correct greeting message.

    Args:
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    hello()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert captured.out == f"{GREETING_MESSAGE}\n"


def test_hello_prints_no_errors(capsys: object) -> None:
    """Test that hello() produces no error output.

    Args:
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    hello()
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert captured.err == ""


def test_cli_main_command_succeeds() -> None:
    """Test that the CLI main command executes successfully."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0


def test_cli_main_command_outputs_greeting() -> None:
    """Test that the CLI main command outputs the greeting message."""
    result = runner.invoke(app, [])
    assert GREETING_MESSAGE in result.stdout


def test_cli_help_command_succeeds() -> None:
    """Test that the CLI --help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_cli_help_shows_description() -> None:
    """Test that the CLI --help shows command description."""
    result = runner.invoke(app, ["--help"])
    assert "Hello World" in result.stdout or "hello" in result.stdout.lower()
