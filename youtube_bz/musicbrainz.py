import aiohttp
import json


async def get_release(mbid):
    """Get MusicBrainz release.

    Parameters
    ----------
    mbid: str
        MusicBrainz Identifier of a release.

    Returns
    -------
    str
        MusicBrainz release object.

    """
    async with aiohttp.ClientSession("https://musicbrainz.org") as session:
        async with session.get(f"/ws/2/release/{mbid}", params={"inc": "artists+recordings", "fmt": "json"}) as response:
            html = await response.text()
            return json.loads(html)
