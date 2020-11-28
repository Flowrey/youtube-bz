import urllib.request
import urllib.parse
import re
import json

from datetime import timedelta

def gen_dict_extract(key: str, var: dict):
    """Search for a specif key inside a nested dictionary.
    https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
    Args:
        key: A string representing the key we are looking for.
        var: A dict in which we search the key.
    Returns:
        result: A yield representing either the dict or the list matching the key.
    """ 

    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

class YoutubeSearch:

    def __init__(self, title, album, artist, generated=True):
        if generated:
            self.q = '+"{}" +"{}" +"{}" +"Auto-generated"'.format(artist, album, title)
        else:
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
        for videoRenderer in gen_dict_extract('videoRenderer', data):
            if 'videoId' in videoRenderer:
                for i in videoRenderer['thumbnailOverlays']:
                    if 'thumbnailOverlayTimeStatusRenderer' in i:
                        video = {}
                        video['title'] = videoRenderer['title']['runs'][0]['text'].lower()
                        video['id'] = videoRenderer['videoId']
                        length = i['thumbnailOverlayTimeStatusRenderer']['text']['simpleText'].split(':')
                        video['length'] = timedelta(minutes = int(length[0]), seconds = int(length[1]))
                        self.results.append(video)
