from __future__ import unicode_literals

import time
import os
import re

from datetime import timedelta

from .api import YoutubeAPI, MusicBrainzAPI
from .album import Album
from .video import Video

from difflib import SequenceMatcher

class YoutubeBZ:

    def search_album(self, artist, album):
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

        regex_artist = re.search(r'(.*) - (.*)', title)
        if regex_artist:
            title = regex_artist.group(2)

        title = title.upper()
        title = re.sub(r'\([^\)]+\)', '', title)
        title = re.sub(r'[\ ]*$', '', title)

        return title

    def compare_title(self, video_title, track_title):

        video_title = self.format_title(video_title)
        track_title = self.format_title(track_title)

        return SequenceMatcher(None, track_title, video_title).ratio()

    def compare_length(self, video_length, track_length):
        video_minutes = int(video_length.split(':')[0])
        video_seconds = int(video_length.split(':')[1])
        video_time = timedelta(minutes = video_minutes, seconds = video_seconds)
        track_time = timedelta(milliseconds = track_length)

        return abs(video_time.seconds - track_time.seconds)

    def find_album(self, mbid: str, genereated: bool = True):

        myAlbum = Album(mbid)

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
                        finded = True
                        break
            if not finded:
               print('# {} [\033[33mFail\033[0m]'.format(track['title']))
            
