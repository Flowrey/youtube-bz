from __future__ import unicode_literals

import urllib.request
import urllib.parse
import mutagen
import threading
import json
import os
import re

from datetime import timedelta
from difflib import SequenceMatcher

from .YoutubeSearch import YoutubeSearch

import youtube_dl

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
    'nocheckcertificate': 'true',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

class Track:

    def __init__(self, title, length, album, artist, tracknumber):
        self.title = title
        self.album = album
        self.length = timedelta(milliseconds = length)
        self.artist = artist
        self.tracknumber = tracknumber

    def match_title(self, video_title):

        music_title = re.sub(r'\'|<|>|/', '', self.title.lower())
        music_title = re.sub(r'\ \(feat\.\ .*\)$', '', self.title.lower())

        video_title = re.sub(r'\'|<|>|/', '', video_title)
        video_title = re.sub(r'\ \(feat\.\ .*\)$', '', video_title)

        if SequenceMatcher(None, music_title, video_title).ratio() > 0.7:
            return True
        return False

    def match_length(self, video_length):
        if abs(video_length.seconds - self.length.seconds) < 10:
            return True
        return False

    def write_tags(self, path):
        audio = mutagen.File(path, easy=True)
        audio['title'] = u'{}'.format(self.title)
        audio['album'] = u'{}'.format(self.album)
        audio['albumartist'] = u'{}'.format(self.artist)
        audio['tracknumber'] = u'{}'.format(self.tracknumber)
        audio.save()

    def find_url(self, videos):
        for video in videos:
            if self.match_title(video['title'].lower()) and self.match_length(video['length']):
                self.url = 'https://www.youtube.com/watch?v=' + video['id']
                return 0
        return 1

    def download(self, videos, path='.'):
        return_code = self.find_url(videos)
        if return_code == 1:
            print('[Error] Can\'t find : {}'.format(self.title))
            return 1
        print('[Downloading] {} : {}'.format(self.title, self.url))

        ydl_opts['outtmpl'] = os.path.join(path, '{}.%(ext)s'.format(self.title))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        print('[Downloaded] {}'.format(self.title))

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
        data = urllib.request.urlopen(url + url_values)
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

        videos = YoutubeSearch(self.title, self.artist).results
        for track in self.tracks:
            x = threading.Thread(target=track.download, args=(videos, self.title,))
            x.start()
