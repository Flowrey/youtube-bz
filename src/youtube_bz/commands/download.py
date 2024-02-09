import concurrent.futures
from dataclasses import dataclass
from typing import Any, Dict, Generator, Optional
from urllib.error import URLError

import pytube
from rich.console import Console

from youtube_bz.api import musicbrainz as MusicBrainzAPI
from youtube_bz.api import youtube as YouTubeAPI
from youtube_bz.api.musicbrainz.api import Track
from youtube_bz.exceptions import YouTubeBrainzError
from youtube_bz.utils.levenshtein_distance import levenshtein_distance


@dataclass
class VideoMatch:
    title: str
    video_id: str
    levenshtein: int


def get_best_match(
    release: MusicBrainzAPI.Release, track: MusicBrainzAPI.Track
) -> Optional[VideoMatch]:
    """Get YouTube videos corresponding to MusicBrainz tracks."""
    search_query = generate_search_query(release, track)

    youtube_client = YouTubeAPI.Client()
    search_results = youtube_client.get_search_results(search_query)
    yt_initial_data = YouTubeAPI.get_initial_data(search_results)

    contents = get_contents(yt_initial_data)
    videos = get_video_distance(track, contents)
    best_matchs = sorted(videos, key=lambda d: d.levenshtein)

    if len(best_matchs) > 0:
        return best_matchs[0]
    return None


def get_contents(yt_initial_data: Dict[str, Any]):
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

    return contents


def get_video_distance(track: Track, contents: Generator[Any, None, None]):
    videos = [
        VideoMatch(
            title=videoRenderer["title"]["runs"][0]["text"],
            video_id=videoRenderer["videoId"],
            levenshtein=levenshtein_distance(
                track["title"].lower(), videoRenderer["title"]["runs"][0]["text"]
            ),
        )
        for videoRenderer in contents
    ]

    return videos


def download_video_audio(title: str, video_id: str, destination: Optional[str] = None):
    if stream := pytube.YouTube(
        f"http://youtube.com/watch?v={video_id}",
    ).streams.get_audio_only():
        stream.download(output_path=destination)


def generate_search_query(
    release: MusicBrainzAPI.Release, track: MusicBrainzAPI.Track
) -> str:
    return (
        f'"{release["artist-credit"][0]["name"]}" "{track["title"]}" "Auto-generated"'
    )


def download_best_match(
    release: MusicBrainzAPI.Release,
    track: MusicBrainzAPI.Track,
    destination: Optional[str],
):
    if res := get_best_match(release, track):
        download_video_audio(res.title, res.video_id, destination)


def download(mbid: str, verbose: bool, destination: Optional[str] = None):
    musicbrainz_client = MusicBrainzAPI.Client()

    try:
        release = musicbrainz_client.lookup_release(mbid)
    except URLError as e:
        raise YouTubeBrainzError(
            f"Failed to get musicbrainz release: {e.reason}\nVerify the MBID provided..."
        )

    console = Console(highlighter=None)
    with console.status(f'[bold green]Downloading "{release["title"]}"...') as status:
        # Search for the corresping video concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_track = {
                executor.submit(download_best_match, release, t, destination): t
                for t in release["media"][0]["tracks"]
            }
            for future in concurrent.futures.as_completed(future_to_track):
                track = future_to_track[future]
                try:
                    future.result()
                except Exception as exc:
                    console.print(f"[[bold red]Err[/bold red]] {exc}")
                else:
                    console.print(f'[[bold green]Ok[/bold green]] {track["title"]}')
