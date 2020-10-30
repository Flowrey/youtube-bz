from __future__ import unicode_literals

import time
import os
import re

from datetime import timedelta

import youtube_dl

from .api import YoutubeAPI, MusicBrainzAPI
from .album import Album
from .video import Video

from difflib import SequenceMatcher

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

class YoutubeBZ:
    """The main class of the program"""

    downloaded = False

    def search_album(self, artist: str, album: str):
        """Search the MBID of an album on MusicBrainz.
        
        Args:
            artist: A string representing the artist name of the alum.
            album: A string representing the album title.

        Returns:
            str: A string representing the MBID of the album.

        """

        data = MusicBrainzAPI().search('artist', artist, 1)
        print('{:17s} {}'.format('', data['artists'][0]['name']))
        data = MusicBrainzAPI().search('release', '{} AND arid:{}'.format(album, data['artists'][0]['id']), 25)

        releases = []
        for item in data['releases']:
            if any (d['title'] == item['title'] and d['track-count'] == item['track-count'] for d in releases):
                pass
            else:
                releases.append({'title' : item['title'], 'id' : item['id'], 'track-count' : item['track-count']})

        print('{:3s} {:50s} {:2s}'.format('', 'Title', 'Track Count'))
        i = 0
        for track in releases:
            print('{:2d}) {:50s} {:2d}'.format(i, track['title'], int(track['track-count'])))
            i = i + 1

        i = int(input('Select one: '))

        return releases[i]['id']

    def format_title(self, title: str)-> str:
        """Format a title for avoiding error in comparaison.
        
        Args:
            title: A string representing the title to format.

        Returns:
            str: A string representing the title formated.

        """

        regex_artist = re.search(r'(.*) - (.*)', title)
        if regex_artist:
            title = regex_artist.group(2)

        title = title.upper()
        title = re.sub(r'\([^\)]+\)', '', title)
        title = re.sub(r'[\ ]*$', '', title)

        return title

    def compare_title(self, video_title: str, track_title: str)-> float:
        """Compare the video title with the music title.

        Args:
            video_title: A string representing the video title.
            track_title: A string representing the track title.

        Returns:
            float: A float representing the resemblance between both titles.

        """

        video_title = self.format_title(video_title)
        track_title = self.format_title(track_title)

        return SequenceMatcher(None, track_title, video_title).ratio()

    def compare_length(self, video_length: str, track_length: int)-> int:
        """Compre the length bettwen the video and the track.

        Args:
            video_length: A string representing the lenght of the video
                with the format (MM:SS).
            track_length: A integer representing the length of the track.

        Returns:
            int: A integer representing the delta between the length of the video and the track.

        """

        video_minutes = int(video_length.split(':')[0])
        video_seconds = int(video_length.split(':')[1])
        video_time = timedelta(minutes = video_minutes, seconds = video_seconds)
        track_time = timedelta(milliseconds = track_length)

        return abs(video_time.seconds - track_time.seconds)

    
    def my_hook(self, d):
        if d['status'] == 'downloading':
            if self.downloaded == False:
                print('Downloading: {}% \r'.format(int((d['downloaded_bytes']*100) / d['total_bytes'])), end="")
            else:
                print('Extracting: {}% \r'.format(int((d['downloaded_bytes']*100) / d['total_bytes'])), end="")
        elif d['status'] == 'finished':
            if self.downloaded == False:
                print('Downloading: Done')
                self.downloaded = True
            else:
                print('Extracting: Done')
                self.downloaded = False
        elif d['status'] == 'error':
            pass

    def find_album(self, mbid: str, genereated: bool = True, download: bool = True):
        """Find and download all the music videos associated to an album on MusicBrainz

        Args:
            mbid: A string representing the MBID of the album to download.
            generated: A boolean indicating if we search for video auto-generated
                by Youtube (True) or if we search over all Youtube (False).
            download: A booleand indicating if we want to download the musics or not.

        """

        myAlbum = Album(mbid)
        ydl_opts = {
                'quiet':True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'progress_hooks': [self.my_hook],
                'logger': MyLogger(),
        }

        for track in myAlbum.tracks:
            if genereated:
                query = '+"{}" +"{}" +"{}" +"Auto-generated"'.format(myAlbum.artist, myAlbum.title, track['title'])
            else:
                query = '+"{}" +"{}"'.format(myAlbum.artist, track['title'])

            videos = YoutubeAPI().search(query)
            
            finded = False
            for video in videos['items']:
                myVideo = Video(video)

                if self.compare_length(myVideo.length, track['length']) < 15:
                    if self.compare_title(myVideo.title, track['title']) > 0.8:
                        print('# {} [\033[32mOK\033[0m]'.format(track['title']))
                        print('https://www.youtube.com/watch?v=' + myVideo.id)
                        if download == True:
                            try:
                                os.mkdir(myAlbum.title)
                            except FileExistsError:
                                pass
                            ydl_opts['outtmpl'] = '{}.%(ext)s'.format(os.path.join(myAlbum.title,track['title']))
                            # FIXME: This is really not an elegant way to do this
                            # but it's the only way i've found to make it work.
                            while True:
                                try:
                                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                        ydl.download(['http://www.youtube.com/watch?v=' + myVideo.id])
                                        break
                                except youtube_dl.DownloadError:
                                        # HACK: Workaround to make youtube_dl works
                                        ydl.download([])
                                        time.sleep(0.5)
                        finded = True
                        break
            if not finded:
               print('# {} [\033[33mFail\033[0m]'.format(track['title']))
            
