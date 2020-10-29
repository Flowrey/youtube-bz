import html

from .api import MusicBrainzAPI

class Video:

    def __init__(self, item: str): 

        self.title = html.unescape(item['snippet']['title'])
        self.length = item['length']
        self.id = item['id']['videoId']
