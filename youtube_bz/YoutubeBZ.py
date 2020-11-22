from __future__ import unicode_literals

import urllib.request
import urllib.parse
import json
import os
import re

from datetime import timedelta
from difflib import SequenceMatcher

from .YoutubeSearch import YoutubeSearch

import youtube_dl
import mutagen

ydl_opts = {
    'format': 'bestaudio/best',
    'nooverwrites' : True,
    'keepvideo' : True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
    }],
}

class Track:

    def __init__(self, title, length, album, artist, tracknumber):
        self.title = title.lower()
        self.album = album.lower()
        self.length = timedelta(milliseconds = length)
        self.artist = artist.lower()
        self.tracknumber = tracknumber

    def match_title(self, video_title):
        ratio = SequenceMatcher(None, self.title, video_title).ratio()
        if ratio > 0.7:
            return True
        elif self.title in video_title:
            return True
        else:
            return False

    def match_length(self, video_length):
        delta = abs(video_length.seconds - self.length.seconds)
        if delta < 10:
            return True
        else:
            return False

    def find_url(self):
        for video in YoutubeSearch(self.title, self.album, self.artist).results:
            if self.match_title(video['title']) and self.match_length(video['length']):
                self.url = 'https://www.youtube.com/watch?v=' + video['id']
                return 0
        return 1

    def write_tags(self, path):
        audio = mutagen.File(path)
        audio['title'] = u'{}'.format(self.title)
        audio['album'] = u'{}'.format(self.album)
        audio['albumartist'] = u'{}'.format(self.artist)
        audio['tracknumber'] = u'{}'.format(self.tracknumber)
        audio.save()

    def my_hook(self, d):
        if d['status'] == 'finished':
            pass

    def download(self, path='.'):
        if self.find_url() == 1:
            print('[youtube-bz] Can\'t find {}'.format(self.title))
            return 1
        ydl_opts['outtmpl'] = os.path.join(path, '{}.%(ext)s'.format(self.title))
        ydl_opts['progress_hooks'] = [self.my_hook]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        for file_name in os.listdir(path):
            if not file_name.split('.')[-1] == 'webm':
                re_file = re.match(r'{}\.(.*)'.format(self.title), file_name)
                if re_file:
                    self.write_tags(os.path.join(path, re_file.group(0)))

class Release:

    def __init__(self, mbid):
        self.__mbid = mbid
        self.tracks = []
        self.__parse()

    def __request(self):
        url = 'https://musicbrainz.org/ws/2/release/{}?'.format(self.__mbid)
        args = {'inc': 'artists+recordings', 'fmt': 'json'}
        url_values = urllib.parse.urlencode(args)
        full_url = url + url_values
        data = urllib.request.urlopen(full_url)
        return data.read()

    def __parse(self):
        data = json.loads(self.__request())
        self.title = data['title']
        self.artist = data['artist-credit'][0]['name']
        self.tracks = [Track(tracks['title'], tracks['length'], self.title, self.artist, tracks['position']) for tracks in data['media'][0]['tracks']]

    def download_album(self):
        try:
            os.mkdir(self.title)
        except FileExistsError:
            pass

        for track in self.tracks:
            track.download(self.title)
