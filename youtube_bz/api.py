import requests
import json
import re

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

        fake_response = {
                            'items':
                            [
                                {
                                    'snippet':
                                    {
                                        'title':'Fake Title'
                                    },
                                    'id':
                                    {
                                        'videoId':'Fake ID'
                                    }
                                }
                            ]
                        }

        r = requests.get(url, params=payload)
        data = re.search(r'(var\ ytInitialData\ =\ )(.*);', r.text).group(2)
        data = json.loads(data)
        contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

        for content in contents:
            if 'videoRenderer' in content:
                fake_response['items'][0]['snippet']['title'] = content['videoRenderer']['title']['runs'][0]['text']
                fake_response['items'][0]['id']['videoId'] = content['videoRenderer']['videoId']
                break

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
        url = 'https://musicbrainz.org/ws/2/{}/{}'.format(entity_type, mbid)
        payload = {
            'fmt':'json',
            'limit':limit,
            'query':query,
        }

        r = requests.get(url, params=payload)
        return r.json()
