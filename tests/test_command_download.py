import pytest
import pytube
import json
import aiohttp
from unittest.mock import patch
from youtube_bz.commands.download import get_best_match, download_video_audio, download
from youtube_bz.api.musicbrainz import Release, Track, ArtistCredit, Media

@pytest.mark.asyncio
@patch("youtube_bz.commands.download.YouTubeAPI.Client.get_search_results")
async def test_get_no_best_match(mock_search_results):
    yt_initial_data = json.dumps({
        "contents":{
            "twoColumnSearchResultsRenderer": {
                "primaryContents": {
                    "sectionListRenderer": {
                        "contents": [{"itemSectionRenderer":{"contents":[]}}]
                    }
                }
            }
        }
    })
    mock_search_results.return_value = f'var ytInitialData = {yt_initial_data};</script><script'
    artist_credit: ArtistCredit = {"name": "foo"}
    track : Track = {"title":"foo", "position":1}
    media : Media = {"tracks":[track]}
    release: Release = {"artist-credit":[artist_credit], "media":[media], "title":"bar"}
    await get_best_match(release, track)

@pytest.mark.asyncio
@patch("youtube_bz.commands.download.YouTubeAPI.Client.get_search_results")
async def test_get_best_match(mock_search_results):
    yt_initial_data = json.dumps({
        "contents":{
            "twoColumnSearchResultsRenderer": {
                "primaryContents": {
                    "sectionListRenderer": {
                        "contents": [{"itemSectionRenderer":{"contents": [
                            {   
                                "videoRenderer": {
                                    "title":{"runs":[{"text":"bar"}]},
                                    "videoId": "bar",
                                },
                            },

                        ]}}]}}
                    }
                }
            })
    mock_search_results.return_value = f'var ytInitialData = {yt_initial_data};</script><script'
    artist_credit: ArtistCredit = {"name": "foo"}
    track : Track = {"title":"foo", "position":1}
    media : Media = {"tracks":[track]}
    release: Release = {"artist-credit":[artist_credit], "media":[media], "title":"bar"}
    await get_best_match(release, track)

@pytest.mark.asyncio
@patch("youtube_bz.commands.download.YouTubeAPI.Client.get_search_results")
async def test_fail_get_best_match(mock_search_results):
    mock_search_results.side_effect = aiohttp.ClientError()
    artist_credit: ArtistCredit = {"name": "foo"}
    track : Track = {"title":"foo", "position":1}
    media : Media = {"tracks":[track]}
    release: Release = {"artist-credit":[artist_credit], "media":[media], "title":"bar"}
    with pytest.raises(aiohttp.ClientError):
        await get_best_match(release, track)

@patch("youtube_bz.commands.download.pytube.YouTube", autospec=pytube.YouTube)
def test_download_video_audio(*_):
    download_video_audio("AmEN!", "2TjcPpasesA")

@pytest.mark.asyncio
@patch("youtube_bz.commands.download.pytube.YouTube", autospec=pytube.YouTube)
@patch("youtube_bz.commands.download.MusicBrainzAPI.Client.lookup_release")
@patch("youtube_bz.commands.download.YouTubeAPI.Client.get_search_results")
async def test_download(mock_search_results, mock_lookup_release, *_):
    yt_initial_data = json.dumps({
        "contents":{
            "twoColumnSearchResultsRenderer": {
                "primaryContents": {
                    "sectionListRenderer": {
                        "contents": [{"itemSectionRenderer":{"contents": [
                            {   
                                "videoRenderer": {
                                    "title":{"runs":[{"text":"bar"}]},
                                    "videoId": "bar",
                                },
                            },

                        ]}}]}}
                    }
                }
            })
    mock_search_results.return_value = f'var ytInitialData = {yt_initial_data};</script><script'
    
    artist_credit: ArtistCredit = {"name": "foo"}
    track : Track = {"title":"foo", "position":1}
    media : Media = {"tracks":[track]}
    release: Release = {"artist-credit":[artist_credit], "media":[media], "title":"bar"}
    mock_lookup_release.return_value = release

    await download("", False)