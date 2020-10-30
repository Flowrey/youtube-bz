import requests
import json
import re

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

class YoutubeAPI:
    """Allow us to perform search on YouTube.

    Regex is used to extract the var containing the JSON data
    in which we can find all the attributes of the video.
    """

    def search(self, q: str) -> str:
        """Search for a video on YouTube

        Args:
            q: A string representing the query.

        Returns:
            fake_response: A string emulating a true response from YouTube API.
        """
        url = 'https://www.youtube.com/results'
        payload = {'search_query': q}

        fake_response = {'items':[]}

        while True:
            try:
                r = requests.get(url, params=payload)
                data = re.search(r'(var\ ytInitialData\ =\ )(.*);', r.text).group(2)
                break
            except AttributeError:
                pass

        data = json.loads(data)
        for videoRenderer in gen_dict_extract('videoRenderer', data):
            if 'videoId' in videoRenderer:
                for i in videoRenderer['thumbnailOverlays']:
                    if 'thumbnailOverlayTimeStatusRenderer' in i:
                        fake_response['items'].append({
                            'snippet':{'title':videoRenderer['title']['runs'][0]['text']},
                            'id':{'videoId':videoRenderer['videoId']}, 
                            'length': i['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
                        })

        return fake_response

class MusicBrainzAPI:
    """Allow to do GET requests to MusciBrainz API. either lookup for an entity based
    on his MBID or search from an entity based on a query.

    """

    def lookup(self, entity_type: str, mbid: str, inc: str) -> str:
        """Lookup for a entity based on his MBIS.
        
        Args:
            entity_type: A string representing core entites in MusicBrainz database.
                (area, artist, event, genre, instrument, label, place, recording, release, release-group, series, work, url)
            mbid: A string representing a 36 characters UUID assigned to an entity in the MusicBrainz database.
            inc: A string who allows to request more information to be included about the entity.

        """

        url = 'https://musicbrainz.org/ws/2/{}/{}'.format(entity_type, mbid)
        payload = {
            'fmt':'json',
            'inc':inc,
        }

        r = requests.get(url, params=payload)
        return r.json()

    def search(self, entity_type: str, query: str, limit: int) -> str:
        """Search for a entity based on a query.
        
        Args:
            entity_type: A string representing core entites in MusicBrainz database.
                (area, artist, event, genre, instrument, label, place, recording, release, release-group, series, work, url).
            query: A string representing the entitie we are looking for.
            limit: A integer representing who much data we want to request.

        """

        url = 'https://musicbrainz.org/ws/2/{}'.format(entity_type)
        payload = {
            'fmt':'json',
            'limit':limit,
            'query':query,
        }

        r = requests.get(url, params=payload)
        return r.json()
