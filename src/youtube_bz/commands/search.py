from typing import Optional

from rich.console import Console
from rich.table import Table

from youtube_bz.api import musicbrainz as MusicBrainzAPI


def search(
    query: str,
    verbose: bool,
    artist: Optional[str] = None,
    artistname: Optional[str] = None,
):
    client = MusicBrainzAPI.Client()
    results = client.search_release(query, artistname=artistname, artist=artist)

    if len(results["releases"]) == 0:
        print("No data to display")
        return

    table = Table(title="Seach Results")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("Score")

    for r in results["releases"]:
        table.add_row(
            f'[bold blue][link=https://musicbrainz.org/release/{r["id"]}]{r["id"]}[/link][/bold blue]',
            r["title"],
            r["artist-credit"][0]["name"],
            str(r["score"]),
        )

    console = Console()
    console.print(table)
