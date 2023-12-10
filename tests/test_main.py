import importlib.metadata
from argparse import Namespace
from unittest.mock import Mock, patch

import pytest

from youtube_bz.main import cli, run_command


def test_get_version(capsys):
    with pytest.raises(SystemExit):
        cli(["--version"])

    captured = capsys.readouterr()
    assert captured.out.strip() == importlib.metadata.version("youtube-bz")


def test_print_help(capsys):
    assert cli([]) == 1


@patch("youtube_bz.main.commands.download")
def test_run_download_cmd(mock_download: Mock):
    cli(["download", "mbid", "--verbose"])
    mock_download.assert_called_once()


@patch("youtube_bz.main.commands.search")
def test_run_search_cmd(mock_search: Mock):
    cli(["search", "query", "--verbose"])
    mock_search.assert_called_once()


def test_run_failed_cmd(capsys):
    assert cli(["download", "bad_mbid", "--verbose"]) == 1


def test_run_unk_cmd(capsys):
    ns = Namespace(command="foo")
    run_command(ns)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Unknown command foo"


@patch("youtube_bz.main.get_command_parser")
def test_unk_exception(mock_parser):  # type: ignore
    with pytest.raises(KeyError):
        mock_parser.side_effect = KeyError("foo")
        cli([])
