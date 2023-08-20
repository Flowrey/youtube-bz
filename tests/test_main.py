from unittest.mock import patch, Mock
import pytest
from argparse import Namespace
from youtube_bz.main import cli, run_command
from youtube_bz.version import __version__

def test_get_version(capsys):
    with pytest.raises(SystemExit):
        cli(["--version"])

    captured = capsys.readouterr()
    assert captured.out.strip() == __version__

def test_print_help(capsys):
    cli([])

def test_verbose(capsys):
    cli(["download", "mbid", "--verbose"])

@pytest.mark.asyncio
async def test_run_unk_cmd(capsys):
    ns = Namespace(command="foo")
    await run_command(ns)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Unknown command foo"

@patch("youtube_bz.main.get_command_parser")
def test_unk_exception(mock_parser):
    with pytest.raises(KeyError):
        mock_parser.side_effect=KeyError('foo')
        cli([])