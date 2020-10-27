import sys

from .api import YoutubeAPI, MusicBrainzAPI
from .album import Album
from .YoutubeBZ import YoutubeBZ

def main():
    if len(sys.argv) < 2:
        mbid = YoutubeBZ().search_albums()
    else:
        mbid = sys.argv[1]
    
    YoutubeBZ().find_ids(mbid)
