import asyncio
import unittest
import youtube_bz


mbid_list = [
    'a17a48b6-51db-3c52-8fdd-066fb9989f78',
    '6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9',
]


class TestYoutubeBrainz(unittest.IsolatedAsyncioTestCase):

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
