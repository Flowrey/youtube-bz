import aiohttp
from pydantic import BaseModel, Field
from typing import List


class ArtistCredit(BaseModel):
    name: str


class Track(BaseModel):
    title: str
    position: int


class Media(BaseModel):
    tracks: List[Track]


class Release(BaseModel):
    artist_credit: List[ArtistCredit] = Field(alias="artist-credit")
    media: List[Media]
    title: str

    @staticmethod
    async def from_mbid(mbid: str):
        """Get MusicBrainz release.

        Parameters
        ----------
        mbid: str
            MusicBrainz Identifier of a release.

        Returns
        -------
        Release
            MusicBrainz release object.

        """
        async with aiohttp.ClientSession("https://musicbrainz.org") as session:
            async with session.get(
                f"/ws/2/release/{mbid}",
                headers={"User-Agent": "YoutubeBrainz/0.1.0"},
                params={"inc": "artists+recordings", "fmt": "json"},
            ) as response:
                data = await response.json()
        return Release(**data)
