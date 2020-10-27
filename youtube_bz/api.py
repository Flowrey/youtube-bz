import requests
import json
import re

def gen_dict_extract(key, var):
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

class F_ckYoutubeAPI:

    __api_key = 'nop'

    def search(self, q: str, maxResults: int = 1) -> str:
        url = 'https://www.googleapis.com/youtube/v3/search'
        payload = {
            'part': 'snippet',
            'maxResults': maxResults,
            'q': q,
            'key': self.__api_key,
            'fields': 'items/id/videoId, items/snippet/title'
        }

        r = requests.get(url, params=payload)
        return r.json()

class YoutubeAPI:

    def search(self, q: str) -> str:
        url = 'https://www.youtube.com/results'
        payload = {'search_query': q}

        fake_response = {'items':[]}

        r = requests.get(url, params=payload)
        data = re.search(r'(var\ ytInitialData\ =\ )(.*);', r.text).group(2)
        data = json.loads(data)
        for videoRenderer in gen_dict_extract('videoRenderer', data):
            if 'videoId' in videoRenderer:
                fake_response['items'].append({'snippet':{'title':videoRenderer['title']['runs'][0]['text']},
                                        'id':{'videoId':videoRenderer['videoId']}})

        return fake_response

class MusicBrainzAPI:

    def lookup(self, entity_type: str, mbid: str, inc: str) -> str:
        url = 'https://musicbrainz.org/ws/2/{}/{}'.format(entity_type, mbid)
        payload = {
            'fmt':'json',
            'inc':inc,
        }

        r = requests.get(url, params=payload)
        return r.json()

    def search(self, entity_type: str, query: str, limit: int) -> str:
        url = 'https://musicbrainz.org/ws/2/{}'.format(entity_type)
        payload = {
            'fmt':'json',
            'limit':limit,
            'query':query,
        }

        r = requests.get(url, params=payload)
        return r.json()
