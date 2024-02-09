import json
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, TypedDict, cast


class ArtistCredit(TypedDict):
    """A MusicBrainz ArtistCredit."""

    name: str


class Track(TypedDict):
    """A MusicBrainz Track."""

    title: str
    position: int


class Media(TypedDict):
    """A MusicBrainz Media."""

    tracks: List[Track]


Release = TypedDict(
    "Release",
    {
        "artist-credit": List[ArtistCredit],
        "media": List[Media],
        "title": str,
        "score": int,
        "id": str,
    },
)


class SearchResult(TypedDict):
    releases: List[Release]


class Client:
    """MusicBrainz API client."""

    _base: str

    def __init__(self, base: str = "https://musicbrainz.org"):
        """Create a new MusicBrainz client."""
        self._base = base

    def _lookup(self, entity_type: str, mbid: str) -> Dict[str, Any]:
        url = f"{self._base}/ws/2/{entity_type}/{mbid}?"
        url += urllib.parse.urlencode({"inc": "artists+recordings", "fmt": "json"})
        with urllib.request.urlopen(url) as response:
            return json.load(response)

    def _search(self, entity_type: str, query: str) -> Dict[str, Any]:
        url = f"{self._base}/ws/2/{entity_type}?"
        url += urllib.parse.urlencode({"query": query, "fmt": "json"})
        with urllib.request.urlopen(url) as response:
            return json.load(response)

    def lookup_release(self, mbid: str) -> Release:
        """Lookup for a release with it's MBID."""
        return cast(Release, self._lookup("release", mbid))

    def search_release(
        self, query: str, artist: Optional[str] = None, artistname: Optional[str] = None
    ) -> SearchResult:
        """Lookup for a release with it's MBID."""
        if artist:
            query += " AND artist=" + artist
        if artistname:
            query += " AND artistname=" + artistname
        return cast(SearchResult, self._search("release", query))
