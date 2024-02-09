import json
import re
import urllib.parse
import urllib.request
from typing import Any, Dict

from .exceptions import FailedToParseIntialData


class Client:
    """YouTube API client."""

    _base: str

    def __init__(self, base: str = "https://youtube.com"):
        self._base = base

    def get_search_results(self, search_query: str) -> str:
        """Get YouTube search results."""
        url = urllib.parse.urljoin(
            self._base, f"/results?search_query={urllib.parse.quote(search_query)}"
        )
        with urllib.request.urlopen(url) as response:
            html = response.read().decode(response.headers.get_content_charset())
        return html


def get_initial_data(search_results: str) -> Dict[str, Any]:
    """Get YouTube initial data."""
    initial_data_regex = re.compile(r"(var\ ytInitialData\ =\ )(.*);</script><script")
    match = initial_data_regex.search(search_results)
    if not match:
        raise FailedToParseIntialData
    return json.loads(match.group(2))
