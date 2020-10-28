import sys
import argparse
import re

from .api import YoutubeAPI, MusicBrainzAPI
from .album import Album
from .YoutubeBZ import YoutubeBZ

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-d', '--download', help='download the album', action='store_true')
    group.add_argument('-m', '--mbid', metavar=('MBID'), help='the mbid of the album')
    group.add_argument('-s', '--search', nargs=2, metavar=('artist', 'album') )

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.search:
        artist, album = args.search
        mbid = YoutubeBZ().search_albums(artist, album)
    else:
        if re.search(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', args.mbid) == None:
            sys.exit('{} not a valid MBID'.format(args.mbid))
        mbid = args.mbid

    YoutubeBZ().find_ids(mbid, args.download)
