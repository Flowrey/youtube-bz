import aiohttp
import json
import re


class YouTube:
    def __init__(self):
        self.url = "https://www.youtube.com"
        self.search_query = None
        self.search_resuls = None
        self.initial_data = None

    def get_search_query(self, release, track):
        """Generate a search query for YouTube.

        Parameters
        ----------
        release : dict
            MusicBrainz release object.
        track : dict
            MusicBrainz track object.

        Returns
        -------
        str
            A search query for YouTube.
        """
        if self.search_query is None:
            self.search_query = f'"{release["artist-credit"][0]["name"]}" "{track["title"]}" "Auto-generated"'
        return self.search_query

    async def get_search_results(self, search_query):
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
        if self.search_resuls is None:
            async with aiohttp.ClientSession(self.url) as session:
                async with session.get("/results", params={"search_query": search_query}) as response:
                    self.search_results = await response.text()
        return self.search_results

    def get_intital_data(self, search_results):
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
        if self.initial_data is None:
            regex = r"(var\ ytInitialData\ =\ )(.*);</script><script"
            initial_data_match = re.search(regex, search_results).group(2)
            self.initial_data = json.loads(initial_data_match)
        return self.initial_data
