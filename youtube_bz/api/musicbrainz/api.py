from typing import Any, TypedDict, cast

from aiohttp import ClientSession


class ArtistCredit(TypedDict):
    """A MusicBrainz ArtistCredit."""

    name: str


class Track(TypedDict):
    """A MusicBrainz Track."""

    title: str
    position: int


class Media(TypedDict):
    """A MusicBrainz Media."""

    tracks: list[Track]


Release = TypedDict(
    "Release", {"artist-credit": list[ArtistCredit], "media": list[Media], "title": str}
)


class Client:
    """MusicBrainz API client."""

    _session: ClientSession

    @classmethod
    async def new(cls, host: str = "https://musicbrainz.org"):
        """Create a new MusicBrainz client."""
        self = cls()
        self._session = ClientSession(
            base_url=host,
            raise_for_status=True,
            headers={"User-Agent": "YoutubeBrainz/0.1.0"},
        )

        return self

    async def _lookup(self, entity_type: str, mbid: str) -> dict[str, Any]:
        async with self._session.get(
            f"/ws/2/{entity_type}/{mbid}",
            params={"inc": "artists+recordings", "fmt": "json"},
        ) as response:
            return await response.json()

    async def lookup_release(self, mbid: str) -> Release:
        """Lookup for a release with it's MBID."""
        return cast(Release, await self._lookup("release", mbid))

    async def close(self) -> None:
        """Close client session."""
        await self._session.close()
