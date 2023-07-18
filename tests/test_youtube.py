from unittest import IsolatedAsyncioTestCase
from youtube_bz.youtube import get_intital_data
from youtube_bz.exceptions import FailedToParseYtIntialData


class TestYoutube(IsolatedAsyncioTestCase):
    async def test_raise_failed_to_parse_yt_initial_data(self):
        data = "non_initial_data_regex"
        with self.assertRaises(FailedToParseYtIntialData):
            get_intital_data(data)
