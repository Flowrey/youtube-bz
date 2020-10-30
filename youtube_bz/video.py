import html

from .api import MusicBrainzAPI

class Video:
    """Strucutre of an YouTube video.

    Attributes:
        title: A string corresponding to the video title.
        length: A string corresponding to the length of the video (MM:SS).
        id: A string corresponding to the id of the video
    """

    def __init__(self, item: str): 
        """Inits Video with the response of the "YouTube API"

        Args:
            item: A string corresponding to the response of the API
        """

        self.title = html.unescape(item['snippet']['title'])
        self.length = item['length']
        self.id = item['id']['videoId']
