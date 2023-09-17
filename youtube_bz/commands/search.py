from typing import Optional

from youtube_bz.api import musicbrainz as MusicBrainzAPI
from rich.console import Console
from rich.table import Table


async def search(
    query: str, verbose: bool, artist: Optional[str], artistname: Optional[str] = None
):
    client = await MusicBrainzAPI.Client.new()
    results = await client.search_release(query, artistname=artistname, artist=artist)
    await client.close()

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
            f'[link=https://musicbrainz.org/release/{r["id"]}]{r["id"]}[/link]', 
            r["title"], 
            r["artist-credit"][0]["name"], 
            str(r["score"])
        )

    console = Console()
    console.print(table)
