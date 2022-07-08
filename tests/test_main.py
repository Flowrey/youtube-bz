import asyncio
import youtube_bz

from unittest import IsolatedAsyncioTestCase

mbid_list = [
    "a17a48b6-51db-3c52-8fdd-066fb9989f78",
    "6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9",
    "b58549a2-0684-4808-9138-a2b4ad70631d",
]


class TestYoutubeBrainz(IsolatedAsyncioTestCase):
    async def test_get_best_match(self):
        for mbid in mbid_list:
            release = await youtube_bz.musicbrainz.get_release(mbid)
            tasks = [
                youtube_bz.get_best_match(release, track)
                for track in release["media"][0]["tracks"]
            ]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    self.assertIn("title", result)
                    self.assertIs(str, type(result["title"]))
                    self.assertIn("id", result)
                    self.assertIs(str, type(result["id"]))
                    self.assertRegex(result["id"], r"^[A-z0-9_-]{11}$")

    async def test_empty_match(self):
        release = await youtube_bz.musicbrainz.get_release(
            "b58549a2-0684-4808-9138-a2b4ad70631d"
        )
        for track in release["media"][0]["tracks"]:
            await youtube_bz.get_best_match(release, track)

    async def test_get_yt_search_results(self):
        yt = youtube_bz.YouTube()
        await yt.get_search_results(
            '"Bring Me The Horizon" "MANTRA" "Auto-generated"'
        )

    async def test_get_yt_initial_data(self):
        yt = youtube_bz.YouTube()
        yt_search_results = await yt.get_search_results(
            '"Bring Me The Horizon" "MANTRA" "Auto-generated"'
        )
        yt.get_intital_data(yt_search_results)

    async def test_get_search_query(self):
        yt = youtube_bz.YouTube()
        release = {"artist-credit": [{"name": "Bring Me The Horizon"}]}
        track = {"title": "MANTRA"}
        search_query = yt.get_search_query(release, track)
        assert search_query == '"Bring Me The Horizon" "MANTRA" "Auto-generated"'


def test_main():
    youtube_bz.main(["6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9"])
