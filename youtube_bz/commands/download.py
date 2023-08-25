import asyncio

import aiohttp
import pytube

from youtube_bz.api import musicbrainz as MusicBrainzAPI
from youtube_bz.api import youtube as YouTubeAPI
from youtube_bz.exceptions import YouTubeBrainzError
from youtube_bz.utils.levenshtein_distance import levenshtein_distance


async def get_best_match(release: MusicBrainzAPI.Release, track: MusicBrainzAPI.Track):
    """Get YouTube video corresponding to MusicBrainz track."""
    search_query = generate_search_query(release, track)

    youtube_client = await YouTubeAPI.Client.new()
    try:
        search_results = await youtube_client.get_search_results(search_query)
    except aiohttp.ClientError:
        raise
    finally:
        await youtube_client.close()
    yt_initial_data = YouTubeAPI.get_initial_data(search_results)

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

    if len(best_matchs) > 0:
        return best_matchs[0]
    return None


def download_video_audio(title: str, video_id: str):
    """Download audio of a YouTube video."""
    print("[Downloading] {} : {}".format(title, video_id))
    if stream := pytube.YouTube(
        f"http://youtube.com/watch?v={video_id}"
    ).streams.get_audio_only():
        stream.download()
    print("[Downloaded] {}".format(title))


def generate_search_query(
    release: MusicBrainzAPI.Release, track: MusicBrainzAPI.Track
) -> str:
    """Generate a search query for YouTube."""
    return (
        f'"{release["artist-credit"][0]["name"]}" "{track["title"]}" "Auto-generated"'
    )


async def download(mbid: str, verbose: bool):
    # Get release info from MusicBrainz
    musicbrainz_client = await MusicBrainzAPI.Client.new()

    try:
        release = await musicbrainz_client.lookup_release(mbid)
    except aiohttp.ClientResponseError as e:
        raise YouTubeBrainzError(
            f"Failed to get musicbrainz release: {e.status}, {e.message}\nVerify the MBID provided..."
        )
    finally:
        await musicbrainz_client.close()

    # Search for the corresping video asynchronously
    results = await asyncio.gather(
        *[get_best_match(release, track) for track in release["media"][0]["tracks"]]
    )

    # Run download in thread pool to avoid blocking IO
    for result in results:
        if result:
            loop = asyncio.get_running_loop()
            loop.run_in_executor(
                None, download_video_audio, result["title"], result["id"]
            )
