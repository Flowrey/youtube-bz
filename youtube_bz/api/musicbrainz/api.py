from typing import Any, TypedDict, cast

from aiohttp import ClientSession


class ArtistCredit(TypedDict):
    name: str


class Track(TypedDict):
    title: str
    position: int


class Media(TypedDict):
    tracks: list[Track]


Release = TypedDict(
    "Release", {"artist-credit": list[ArtistCredit], "media": list[Media], "title": str}
)


class Client:
    _host: str
    _session: ClientSession

    @classmethod
    async def new(cls, host: str = "https://musicbrainz.org"):
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
        return cast(Release, await self._lookup("release", mbid))

    async def close(self) -> None:
        await self._session.close()