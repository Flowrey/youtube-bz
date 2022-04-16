import asyncio
import unittest
import youtube_bz


class TestYoutubeBrainz(unittest.IsolatedAsyncioTestCase):

    async def test_match(self):
        release = await youtube_bz.get_musicbrainz_release("6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
        tasks = [youtube_bz.chain_call(release, track) for track in release['media'][0]['tracks']]
        results = await asyncio.gather(*tasks)

        for result in results:
            self.assertIn('title', result)
            self.assertIs(str, type(result['title']))
            self.assertIn('id', result)
            self.assertIs(str, type(result['id']))
            self.assertRegex(result['id'], r'^[A-z0-9_-]{11}$')


if __name__ == '__main__':
    unittest.main()
