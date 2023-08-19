import asyncio
import argparse
import logging
import sys

from youtube_bz import commands
from youtube_bz.exceptions import YouTubeBrainzError

logger = logging.getLogger(__name__)

async def run_command(args: argparse.Namespace):
    match args.command:
        case "download":
            await commands.download(
                args.mbid,
            )
        case _:
            print(f"Unknown command {args.command}")

def get_command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="youtube-bz",
    )

    subparsers = parser.add_subparsers(
        dest="command", description="Get help for commands with youtube-bz COMMAND --help"
    )

    download_parser = subparsers.add_parser(
        "download",
        help="Download a release",
        description="Find and download Youtube Videos associated to a release on MusicBrainz.",
    )
    download_parser.add_argument("mbid", help="music brainz identifer of a release")

    return parser

def cli() -> int:
    try:
        parser = get_command_parser()
        parsed_args = parser.parse_args()
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
    return 0