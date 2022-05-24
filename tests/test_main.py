import asyncio
import youtube_bz

from unittest import IsolatedAsyncioTestCase, mock
from pathlib import Path

mbid_list = [
    'a17a48b6-51db-3c52-8fdd-066fb9989f78',
    '6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9',
    'b58549a2-0684-4808-9138-a2b4ad70631d',
]


def mocked_youtube_dl(*args):
    class MockedYoutubeDL:
        def __init__(self, ydl_opts):
            self.ydl_opts = ydl_opts

        def __enter__(self):
            return self

        def __exit__(sel, *args):
            return

        def download(self, ydl_id_list):
            for i in ydl_id_list:
                Path(self.ydl_opts['outtmpl'] % {'ext': 'mp3'}).touch()

    return MockedYoutubeDL(*args)


class TestYoutubeBrainz(IsolatedAsyncioTestCase):

    async def test_match(self):
        for mbid in mbid_list:
            release = await youtube_bz.get_musicbrainz_release(mbid)
            tasks = [youtube_bz.chain_call(release, track) for track in release['media'][0]['tracks']]
            results = await asyncio.gather(*tasks)

            for result in results:
                self.assertIn('title', result)
                self.assertIs(str, type(result['title']))
                self.assertIn('id', result)
                self.assertIs(str, type(result['id']))
                self.assertRegex(result['id'], r'^[A-z0-9_-]{11}$')

    async def test_empty_match(self):
        release = await youtube_bz.get_musicbrainz_release('b58549a2-0684-4808-9138-a2b4ad70631d')
        for track in release['media'][0]['tracks']:
            search_query = f'"{release["artist-credit"][0]["name"]}" "{release["title"]}" "{track["title"]}" "Auto-generated"'
            search_results = await youtube_bz.get_yt_search_results(search_query)
            yt_initial_data = await youtube_bz.get_yt_intital_data(search_results)
            await youtube_bz.get_best_match(yt_initial_data, track)

    @mock.patch('youtube_dl.YoutubeDL', side_effect=mocked_youtube_dl)
    def test_download(self, mock_youtube_dl):
        youtube_bz.download('The Walls Are Way Too Thin', '36hmuTxo88U')
        self.assertTrue(Path('The Walls Are Way Too Thin.mp3').is_file())

    @mock.patch('youtube_dl.YoutubeDL', side_effect=mocked_youtube_dl)
    def test_main(self, mocked_youtube_dl):
        youtube_bz.main(['6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9'])
