import argparse
import aiohttp
import asyncio
import Levenshtein
import ujson
import youtube_dl
import re
import os


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        pass


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


# Blocking IO
def download(title, video_id):
    # Download matching video
    print('[Downloading] {} : {}'.format(title, video_id))
    ydl_opts['outtmpl'] = os.path.join('.', '{}.%(ext)s'.format(title))
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_id])
    print('[Downloaded] {}'.format(title))


async def find_best_match(release, track):
    # Get youtube results for each track
    search_query = f'"{release["artist-credit"][0]["name"]}" "{release["title"]}" "{track["title"]}" "Auto-generated"'
    async with aiohttp.ClientSession("https://www.youtube.com") as session:
        async with session.get('/results', params={'search_query': search_query}) as response:
            # Get youtube initial data
            html = await response.text()
            yt_initial_data = ujson.loads(re.search(r'(var\ ytInitialData\ =\ )(.*);</script><script', html).group(2))

            print(f"Looking for: {track['title']}")
            # Find best match
            best_distance = None
            best_match = None
            for itemSectionRenderer in yt_initial_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
                if 'videoRenderer' in itemSectionRenderer:
                    video = {'title': itemSectionRenderer['videoRenderer']['title']['runs'][0]['text'], 'id': itemSectionRenderer['videoRenderer']['videoId']}
                    distance = Levenshtein.distance(track['title'].lower(), video['title'].lower())
                    if best_distance is None:
                        best_distance = distance
                        best_match = video
                    if distance < best_distance:
                        best_distance = distance
                        best_match = video

            print(f"Finded: {best_match['title']}")
            # Run download in thread pool
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, download, best_match['title'], best_match['id'])


async def run(mbid):
    # Get musicbrainz release
    async with aiohttp.ClientSession('https://musicbrainz.org') as session:
        async with session.get(f'/ws/2/release/{mbid}', params={'inc': 'artists+recordings', 'fmt': 'json'}) as response:
            html = await response.text()
            release = ujson.loads(html)
            tasks = [find_best_match(release, track) for track in release['media'][0]['tracks']]
            await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Find and download Youtube Videos associated to an Album on MusicBrainz.")
    parser.add_argument('mbid', help="music brainz identifer of a release")
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.mbid))
