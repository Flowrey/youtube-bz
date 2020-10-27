import sys

from .api import YoutubeAPI, MusicBrainzAPI
from .album import Album
from .YoutubeBZ import YoutubeBZ

def main():
    YoutubeBZ().find_ids(sys.argv[1])
