import requests

class YoutubeAPI:

    __api_key = 'MY_API_KEY'

    def search(self, q: str, maxResults: int = 1) -> str:
        url = 'https://www.googleapis.com/youtube/v3/search'
        payload = {
            'part': 'snippet',
            'maxResults': maxResults,
            'q': q,
            'key': self.__api_key,
            'type': 'video',
        }

        r = requests.get(url, params=payload)
        return r.json()

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
