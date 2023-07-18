import json
from unittest import IsolatedAsyncioTestCase
from aiohttp import ClientSession
from youtube_bz.musicbrainz import Release
from unittest.mock import patch


class MockResponse:
    def __init__(self, text: str, status: int):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def json(self):
        return json.loads(self._text)

    async def __aexit__(self, exc_type, exc, tb):  # type: ignore
        pass

    async def __aenter__(self):
        return self


class TestMusicBrainz(IsolatedAsyncioTestCase):
    @patch("aiohttp.ClientSession.get")
    async def test_get_release_from_mbid(self, mock: ClientSession):
        data = """{"title":"amo","media": [],"artist-credit": []}"""
        mock.return_value = MockResponse(data, 200)
        release = await Release.from_mbid("6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
        assert release.title == "amo"
