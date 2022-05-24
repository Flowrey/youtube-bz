import logging
import argparse
import aiohttp
import asyncio
import Levenshtein
import ujson
import youtube_dl
import sys
import re
import os


logging.basicConfig(level=logging.INFO)

ydl_opts = {
    'quiet': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
    }],
}


def download(title, video_id):
    """Download audio of a YouTube video.

    Parameters
    ----------
    title : str
        The track title.
    video_id : str
        The YouTube video id corresponding to the track.

    """
    print('[Downloading] {} : {}'.format(title, video_id))
    ydl_opts['outtmpl'] = os.path.join('.', '{}.%(ext)s'.format(title))
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_id])
    print('[Downloaded] {}'.format(title))


async def get_best_match(yt_initial_data, track):
    """Get YouTube video corresponding to MusicBrainz track.

    Parameters
    ----------
    yt_initial_data : dict
        YouTube initial data.
    track : dict
        MusicBrainz track object.

    Returns
    -------
    dict
        A dict containing the video title and id, matching the track title.

    """
    contents = (
        itemSectionRenderer['videoRenderer']
        for itemSectionRenderer in yt_initial_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        if 'videoRenderer' in itemSectionRenderer
    )
    videos = [
        {
            'title': videoRenderer['title']['runs'][0]['text'],
            'id': videoRenderer['videoId'],
            'levenshtein': Levenshtein.distance(
                track['title'].lower(),
                videoRenderer['title']['runs'][0]['text']
            )
        }
        for videoRenderer in contents
    ]
    best_matchs = sorted(videos, key=lambda d: d['levenshtein'])
    logging.debug(best_matchs)

    if len(best_matchs) > 0:
        return best_matchs[0]
    else:
        return None


async def get_yt_intital_data(search_results):
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
    regex = r'(var\ ytInitialData\ =\ )(.*);</script><script'
    yt_initial_data = re.search(regex, search_results).group(2)
    return ujson.loads(yt_initial_data)


async def get_search_query(release, track):
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
    # search_query = f'"{release["artist-credit"][0]["name"]}" "{release["title"]}" "{track["title"]}" "Auto-generated"'
    search_query = f'"{release["artist-credit"][0]["name"]}" "{track["title"]}" "Auto-generated"'
    return search_query


async def get_yt_search_results(search_query):
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
    async with aiohttp.ClientSession("https://www.youtube.com") as session:
        async with session.get('/results', params={'search_query': search_query}) as response:
            search_results = await response.text()
            return search_results


async def get_musicbrainz_release(mbid):
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
    async with aiohttp.ClientSession('https://musicbrainz.org') as session:
        async with session.get(f'/ws/2/release/{mbid}', params={'inc': 'artists+recordings', 'fmt': 'json'}) as response:
            html = await response.text()
            return ujson.loads(html)


async def chain_call(release, track):
    search_query = await get_search_query(release, track)
    yt_search_results = await get_yt_search_results(search_query)
    yt_initial_data = await get_yt_intital_data(yt_search_results)
    best_match = await get_best_match(yt_initial_data, track)
    return best_match


async def run(mbid):
    release = await get_musicbrainz_release(mbid)
    tasks = [chain_call(release, track) for track in release['media'][0]['tracks']]
    results = await asyncio.gather(*tasks)

    # Run download in thread pool to avoid blocking IO
    for result in results:
        if result:
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, download, result['title'], result['id'])


def main(sys_argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Find and download Youtube Videos associated to an Album on MusicBrainz.")
    parser.add_argument('mbid', help="music brainz identifer of a release")
    args = parser.parse_args(sys_argv)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.mbid))
