import argparse
import asyncio
import importlib.metadata
import logging
import sys

from youtube_bz import commands
from youtube_bz.exceptions import YouTubeBrainzError

logger = logging.getLogger(__name__)


def print_version() -> None:
    print(importlib.metadata.version("youtube-bz"))


async def run_command(args: argparse.Namespace):
    verbose = args.verbose if "verbose" in args else False
    if args.command == "download":
        await commands.download(args.mbid, verbose, args.destination)
    elif args.command == "search":
        await commands.search(
            args.query, verbose, artistname=args.artistname, artist=args.artist
        )
    else:
        print(f"Unknown command {args.command}")


def get_command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="youtube-bz",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        description="Get help for commands with youtube-bz COMMAND --help",
    )

    # download parser
    download_parser = subparsers.add_parser(
        "download",
        help="Download a release",
        description="Find and download Youtube Videos associated to a release on MusicBrainz.",
    )
    download_parser.add_argument("mbid", help="music brainz identifer of a release")
    download_parser.add_argument("--verbose", action="store_true")

    download_parser.add_argument(
        "-d", "--destination", help="Path to the output directory"
    )

    # search parser
    search_parser = subparsers.add_parser(
        "search",
        help="Search a release",
        description="Find a release on MusicBrainz.",
    )
    search_parser.add_argument("query", help="Lucene search query")
    search_parser.add_argument(
        "--artist",
        help='(part of) the combined credited artist name for the release, including join phrases (e.g. "Artist X feat.")',
    )
    search_parser.add_argument(
        "--artistname", help="(part of) the name of any of the release artists "
    )

    # main parser
    parser.add_argument("--version", action="store_true", help="Print version and exit")

    return parser


def setup_logging(verbose: bool) -> None:
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


def setup(args: argparse.Namespace) -> None:
    if "version" in args and args.version:
        print_version()
        sys.exit(0)

    setup_logging("verbose" in args and args.verbose)


def cli(args: list[str] = sys.argv[1:]):
    try:
        parser = get_command_parser()
        parsed_args = parser.parse_args(args)
        setup(parsed_args)
        if not parsed_args.command:
            parser.print_help()
            return 1
        asyncio.run(run_command(parsed_args))
    except YouTubeBrainzError as e:
        print(str(e), file=sys.stderr)
        logger.debug(f"YouTubeBrainzError: {e}", exc_info=True)
        return 1
    except Exception:
        logger.debug("Uncaught Exception:", exc_info=True)
        raise
