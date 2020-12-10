import urllib.request
import urllib.parse
import re
import json

from datetime import timedelta

class YoutubeSearch:

    def __init__(self, title, album, artist, mode=0):

        if mode == 0:
            self.q = 'intitle:"{} +"Auto-generated" +"{}"'.format(title, artist)
        elif mode == 1:
            self.q = '+"{}" +"{}" +"{}" +"Auto-generated"'.format(artist, album, title)
        elif mode == 2:
            self.q = '+"{}" +"{}" +"{}"'.format(artist, album, title)

        self.results = []
        self.__parse()
        
    def __request(self):
        url = 'https://www.youtube.com/results?'
        args = {'search_query': self.q}
        url_values = urllib.parse.urlencode(args)
        full_url = url + url_values
        data = urllib.request.urlopen(full_url)
        data = data.read().decode('utf-8')
        return re.search(r'(var\ ytInitialData\ =\ )(.*);</script>', data).group(2)

    def __parse(self):
        data = json.loads(self.__request())
        for videos in data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
            video = {}
            if 'videoRenderer' in videos:
                video['title'] = videos['videoRenderer']['title']['runs'][0]['text'].lower()
                video['id'] = videos['videoRenderer']['videoId']
                video['chanel'] = videos['videoRenderer']['longBylineText']['runs'][0]['text']
                length = videos['videoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText'].split(':')
                video['length'] = timedelta(minutes = int(length[0]), seconds = int(length[1]))
                self.results.append(video)
            elif 'shelfRenderer' in videos:
                for items in videos['shelfRenderer']['content']['verticalListRenderer']['items']:
                    video['title'] = items['videoRenderer']['title']['runs'][0]['text'].lower()
                    video['id'] = items['videoRenderer']['videoId']
                    video['chanel'] = items['videoRenderer']['longBylineText']['runs'][0]['text']
                    length = items['videoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText'].split(':')
                    video['length'] = timedelta(minutes = int(length[0]), seconds = int(length[1]))
                    self.results.append(video)
