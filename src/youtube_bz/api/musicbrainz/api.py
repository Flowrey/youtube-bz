import json
import urllib.parse
import urllib.request
from typing import Any, TypedDict, cast


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

    _base: str

    def __init__(self, base: str = "https://musicbrainz.org"):
        """Create a new MusicBrainz client."""
        self._base = base

    def _lookup(self, entity_type: str, mbid: str) -> dict[str, Any]:
        url = urllib.parse.urljoin(self._base, f"/ws/2/{entity_type}/{mbid}")
        url += "?inc=artists+recordings&fmt=json"
        with urllib.request.urlopen(url) as response:
            html = response.read()
            data = json.loads(html)
        return data

    def lookup_release(self, mbid: str) -> Release:
        """Lookup for a release with it's MBID."""
        return cast(Release, self._lookup("release", mbid))
