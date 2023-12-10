from unittest.mock import Mock, patch

from youtube_bz import commands


@patch("youtube_bz.api.musicbrainz.Client.search_release")
def test_search_command(search_mock: Mock):
    search_mock.return_value = {
        "releases": [
            {
                "title": "amo",
                "media": [],
                "artist-credit": [{"name": "bmth"}],
                "id": "0000",
                "score": 100,
            }
        ]
    }
    commands.search("query", False)
    search_mock.assert_called_once()


@patch("youtube_bz.api.musicbrainz.Client.search_release")
def test_search_command_no_results(search_mock: Mock, capsys):
    search_mock.return_value = {"releases": []}
    commands.search("query", False)
    search_mock.assert_called_once()
    capured = capsys.readouterr()
    assert "No data to display\n" == capured.out
