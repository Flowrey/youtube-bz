import urllib.request
import json

class BrainzSearch:

    def __init__(self, artist, album):
        self.artist = artist
        self.album = album
        self.releases = []

    def __request_artist(self):
        url = 'https://musicbrainz.org/ws/2/artist?'
        args = {'query':self.artist, 'fmt': 'json'}
        url_values = urllib.parse.urlencode(args)
        full_url = url + url_values
        data = urllib.request.urlopen(full_url)
        return data.read()

    def __request_album(self):
        self.__parse_artist()
        url = 'https://musicbrainz.org/ws/2/release?'
        args = {'query':self.album + 'AND arid:' + self.arid, 'fmt': 'json'}
        url_values = urllib.parse.urlencode(args)
        full_url = url + url_values
        data = urllib.request.urlopen(full_url)
        return data.read()

    def __parse_artist(self):
        data = json.loads(self.__request_artist())
        self.arid = data['artists'][0]['id']

    def __parse_album(self):
        data = json.loads(self.__request_album())
        for item in data['releases']:
            if any (d['title'] == item['title'] and d['track-count'] == item['track-count'] for d in self.releases):
                pass
            else:
                self.releases.append({'title' : item['title'], 'id' : item['id'], 'track-count' : item['track-count']})

    def select_album(self):
        self.__parse_album()
        print('{:3s} {:50s} {:2s}'.format('', 'Title', 'Track Count'))
        i = 0
        for track in self.releases:
            print('{:2d}) {:50s} {:2d}'.format(i, track['title'], int(track['track-count'])))
            i = i + 1

        i = int(input('Select one: '))

        return self.releases[i]['id']
