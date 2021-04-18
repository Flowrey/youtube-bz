import urllib.request
import urllib.parse
import json
import re

from datetime import timedelta

class YoutubeSearch:

    def __init__(self, album, artist):
        self.q = '"{}" "{}" "Auto-generated"'.format(album, artist)
        self.results = []
        self.__parse()
        
    def __request(self):
        url = 'https://www.youtube.com/results?'
        args = {'search_query': self.q}
        url_values = urllib.parse.urlencode(args)
        data = urllib.request.urlopen(url + url_values)
        data = data.read().decode('utf-8')
        return re.search(r'(var\ ytInitialData\ =\ )(.*);</script>', data).group(2)

    def __parse(self):
        data = json.loads(self.__request())
        for videos in data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
            video = {}
            if 'videoRenderer' in videos:
                if 'ownerBadges' in videos['videoRenderer']:
                    views = videos['videoRenderer']['viewCountText']['simpleText']
                    length = videos['videoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText'].split(':')
                    video['title'] = videos['videoRenderer']['title']['runs'][0]['text'].lower()
                    video['id'] = videos['videoRenderer']['videoId']
                    video['chanel'] = videos['videoRenderer']['longBylineText']['runs'][0]['text']
                    video['badge'] = videos['videoRenderer']['ownerBadges'][0]['metadataBadgeRenderer']['icon']['iconType']
                    video['views'] = re.sub("[^0-9]","", views)
                    video['length'] = timedelta(minutes = int(length[0]), seconds = int(length[1]))
                    for i in self.results:
                        if i['title'] == video['title']:
                            if i['views'] > video['views']:
                                self.results.remove(i)
                    self.results.append(video)
