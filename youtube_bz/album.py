from .api import MusicBrainzAPI

class Album:
    """Structure of an album on MusicBrainz.

    Attributes:
        title: A string corresponding to the title of the album.
        artist: A string corresponding to the artist of the album.
        tracks: A list with all the tracks of the album.
    """

    def __init__(self, mbid: str): 
        """Inits Album with a GET requests to MusicBrainz API.

        Args:
            mbid: A string corresponding to the MusicBrainz Identifier of the releases.
        """

        release = MusicBrainzAPI().lookup('release', mbid, 'recordings+artists')

        self.title = release['title']
        self.artist = release['artist-credit'][0]['name']
        self.tracks = []

        for media in release['media']:
            for tracks in media['tracks']:
                self.tracks.append(tracks['title'])
