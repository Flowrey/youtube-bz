from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from aiohttp import ClientSession

from tests.utils import MockResponse
from youtube_bz.api.musicbrainz import Client


class TestMusicBrainz(IsolatedAsyncioTestCase):
    @patch("aiohttp.ClientSession.get")
    async def test_get_release_from_mbid(self, mock: ClientSession):
        data = """{"title":"amo","media": [],"artist-credit": []}"""
        mock.return_value = MockResponse(data, 200)
        client = await Client.new()
        release = await client.lookup_release("6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
        assert release["title"] == "amo"
        await client.close()
