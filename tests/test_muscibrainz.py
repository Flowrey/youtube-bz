from pytest_httpserver import HTTPServer

from youtube_bz.api.musicbrainz import Client


def test_lookup_release_from_mbid(httpserver: HTTPServer):
    data = """{"title":"amo","media": [],"artist-credit": []}"""
    httpserver.expect_request("/ws/2/release/6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9").respond_with_data(data)  # type: ignore
    client = Client(f"http://{httpserver.host}:{httpserver.port}")
    release = client.lookup_release("6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
    assert release["title"] == "amo"


def test_search_release(httpserver: HTTPServer):
    data = """{"releases":[{"title":"amo","media": [],"artist-credit": []}]}"""
    httpserver.expect_request("/ws/2/release", query_string="query=amo+AND+artist%3Dbmth+AND+artistname%3Dbmth&fmt=json").respond_with_data(data)  # type: ignore
    client = Client(f"http://{httpserver.host}:{httpserver.port}")
    res = client.search_release("amo", artist="bmth", artistname="bmth")
    assert res["releases"][0]["title"] == "amo"
