import logging
import argparse
import asyncio
import pytube
import sys

from . import musicbrainz
from .youtube import YouTube
from .utils.levenshtein_distance import levenshtein_distance


def download(title, video_id):
    """Download audio of a YouTube video.

    Parameters
    ----------
    title : str
        The track title.
    video_id : str
        The YouTube video id corresponding to the track.

    """
    print("[Downloading] {} : {}".format(title, video_id))
    yt = pytube.YouTube(f"http://youtube.com/watch?v={video_id}")
    yt.streams.filter(only_audio=True)[-1].download()
    print("[Downloaded] {}".format(title))


async def get_best_match(release, track):
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
    youtube = YouTube()
    search_query = youtube.get_search_query(release, track)
    search_results = await youtube.get_search_results(search_query)
    yt_initial_data = youtube.get_intital_data(search_results)

    contents = (
        itemSectionRenderer["videoRenderer"]
        for itemSectionRenderer in yt_initial_data["contents"][
            "twoColumnSearchResultsRenderer"
        ]["primaryContents"]["sectionListRenderer"]["contents"][0][
            "itemSectionRenderer"
        ][
            "contents"
        ]
        if "videoRenderer" in itemSectionRenderer
    )
    videos = [
        {
            "title": videoRenderer["title"]["runs"][0]["text"],
            "id": videoRenderer["videoId"],
            "levenshtein": levenshtein_distance(
                track["title"].lower(), videoRenderer["title"]["runs"][0]["text"]
            ),
        }
        for videoRenderer in contents
    ]
    best_matchs = sorted(videos, key=lambda d: d["levenshtein"])
    logging.debug(best_matchs)

    if len(best_matchs) > 0:
        return best_matchs[0]
    return None


async def youtube_bz(mbid):
    # Get release info from MusicBrainz
    release = await musicbrainz.get_release(mbid)
    results = await asyncio.gather(*[get_best_match(release, track) for track in release["media"][0]["tracks"]])

    # Run download in thread pool to avoid blocking IO
    for result in results:
        if result:
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, download, result["title"], result["id"])


def main(sys_argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Find and download Youtube Videos associated to an Album on MusicBrainz."
    )
    parser.add_argument("mbid", help="music brainz identifer of a release")
    args = parser.parse_args(sys_argv)
    asyncio.run(youtube_bz(args.mbid))
