import json
import re
from typing import Any

from aiohttp import ClientSession

from .exceptions import FailedToParseIntialData


class Client:
    _host: str
    _session: ClientSession

    @classmethod
    async def new(cls, host: str = "https://www.youtube.com"):
        self = cls()
        self._session = ClientSession(base_url=host, raise_for_status=True)

        return self

    async def get_search_results(self, search_query: str) -> str:
        """Get YouTube search results."""
        async with self._session.get(
            "/results", params={"search_query": search_query}
        ) as response:
            return await response.text()

    async def close(self) -> None:
        await self._session.close()


def get_intital_data(search_results: str) -> dict[str, Any]:
    """Get YouTube initial data."""
    initial_data_regex = re.compile(r"(var\ ytInitialData\ =\ )(.*);</script><script")
    match = initial_data_regex.search(search_results)
    if not match:
        raise FailedToParseIntialData
    return json.loads(match.group(2))
