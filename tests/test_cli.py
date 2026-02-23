"""Tests for CLI module."""

from click.testing import CliRunner

from apk_decompiler.cli import main


def test_main_help():
    """Test main CLI help."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "APK Decompiler CLI" in result.output


def test_main_version():
    """Test main CLI version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_decompile_help():
    """Test decompile command help."""
    runner = CliRunner()
    result = runner.invoke(main, ["decompile", "--help"])
    assert result.exit_code == 0
    assert "Decompile an APK file" in result.output


def test_analyze_help():
    """Test analyze command help."""
    runner = CliRunner()
    result = runner.invoke(main, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze an APK file" in result.output


def test_extract_help():
    """Test extract command help."""
    runner = CliRunner()
    result = runner.invoke(main, ["extract", "--help"])
    assert result.exit_code == 0
    assert "Extract resources" in result.output
