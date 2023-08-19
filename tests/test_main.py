from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import vcr  # type: ignore
from pytube import YouTube

import youtube_bz
from youtube_bz import download
from youtube_bz.musicbrainz import ArtistCredit, Release, Track

mbid_list = [
    "a17a48b6-51db-3c52-8fdd-066fb9989f78",
    "6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9",
    "b58549a2-0684-4808-9138-a2b4ad70631d",
]


class TestYoutubeBrainz(IsolatedAsyncioTestCase):
    async def test_get_yt_search_results(self):
        await youtube_bz.youtube.get_search_results(
            '"Bring Me The Horizon" "MANTRA" "Auto-generated"'
        )

    async def test_get_yt_initial_data(self):
        yt_search_results = await youtube_bz.youtube.get_search_results(
            '"Bring Me The Horizon" "MANTRA" "Auto-generated"'
        )
        youtube_bz.youtube.get_intital_data(yt_search_results)

    async def test_get_search_query(self):
        artist_credit = [ArtistCredit(name="Bring Me The Horizon")]
        release = Release(
            **{"artist-credit": artist_credit, "media": [], "title": "Amo"}  # type: ignore
        )
        track = Track(title="MANTRA", position="2")  # type: ignore
        search_query = youtube_bz.youtube.get_search_query(release, track)
        assert search_query == '"Bring Me The Horizon" "MANTRA" "Auto-generated"'

    @patch("pytube.YouTube", autospec=YouTube)
    async def test_download(self, youtube: YouTube):
        download("AmEN!", "2TjcPpasesA")

    @patch("pytube.YouTube", autospec=YouTube)
    @vcr.use_cassette("fixtures/vcr_cassettes/youtube_bz.yaml")  # type: ignore
    def test_main(self, youtube: YouTube):
        youtube_bz.main(["6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9"])
