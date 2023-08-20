import importlib.metadata
from argparse import Namespace
from unittest.mock import patch

import pytest

from youtube_bz.main import cli, run_command


def test_get_version(capsys):  # type: ignore
    with pytest.raises(SystemExit):
        cli(["--version"])

    captured = capsys.readouterr()  # type: ignore
    assert captured.out.strip() == importlib.metadata.version("youtube-bz")  # type: ignore


def test_print_help(capsys):  # type: ignore
    cli([])


def test_verbose(capsys):  # type: ignore
    cli(["download", "mbid", "--verbose"])


@pytest.mark.asyncio
async def test_run_unk_cmd(capsys):  # type: ignore
    ns = Namespace(command="foo")
    await run_command(ns)
    captured = capsys.readouterr()  # type: ignore
    assert captured.out.strip() == "Unknown command foo"  # type: ignore


@patch("youtube_bz.main.get_command_parser")
def test_unk_exception(mock_parser):  # type: ignore
    with pytest.raises(KeyError):
        mock_parser.side_effect = KeyError("foo")
        cli([])
