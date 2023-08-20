from unittest.mock import patch
from unittest import IsolatedAsyncioTestCase
from aiohttp import ClientSession
from tests.utils import MockResponse

from youtube_bz.api.youtube.exceptions import FailedToParseIntialData
from youtube_bz.api.youtube import Client, get_initial_data


class TestYoutube(IsolatedAsyncioTestCase):
    async def test_raise_failed_to_parse_yt_initial_data(self):
        data = "non_initial_data_regex"
        with self.assertRaises(FailedToParseIntialData):
            get_initial_data(data)

    @patch("aiohttp.ClientSession.get")
    async def test_get_initial_data(self, mock: ClientSession):
        mock.return_value = MockResponse('var ytInitialData = {"foo":"bar"};</script><script', 200)
        client = await Client.new()
        res = await client.get_search_results("Bring Me The Horizon")
        await client.close()
        init_data = get_initial_data(res)
        assert init_data == {"foo":"bar"}
