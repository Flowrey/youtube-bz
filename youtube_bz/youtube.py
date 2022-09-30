import json
import re

import aiohttp
from typing import Any

from .musicbrainz import Release, Track
from .exceptions import FailedToParseYtIntialData


def get_search_query(release: Release, track: Track) -> str:
    """Generate a search query for YouTube.

    Parameters
    ----------
    release : Release
        MusicBrainz release object.
    track : Track
        MusicBrainz track object.

    Returns
    -------
    str
        A search query for YouTube.
    """
    return f'"{release.artist_credit[0].name}" "{track.title}" "Auto-generated"'


async def get_search_results(search_query: str) -> str:
    """Get YouTube search results.

    Parameters
    ----------
    search_query : str
        The query to request to YouTube.

    Returns
    -------
    str
        Raw YouTube search results.

    """
    url = "https://www.youtube.com"
    async with aiohttp.ClientSession(url) as session:
        async with session.get(
            "/results", params={"search_query": search_query}
        ) as response:
            return await response.text()


def get_intital_data(search_results: str) -> dict[Any, Any]:
    """Get YouTube initial data.

    Parameters
    ----------
    search_results : str
        Raw search results containing YouTube initial data.

    Returns
    -------
    dict
        A dict containing the YouTube initial data.

    """
    initial_data_regex = re.compile(r"(var\ ytInitialData\ =\ )(.*);</script><script")
    match = initial_data_regex.search(search_results)
    if not match:
        raise FailedToParseYtIntialData
    return json.loads(match.group(2))
