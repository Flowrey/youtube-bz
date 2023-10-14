from pytest_httpserver import HTTPServer

from youtube_bz.api.musicbrainz import Client


def test_get_release_from_mbid(httpserver: HTTPServer):
    data = """{"title":"amo","media": [],"artist-credit": []}"""
    httpserver.expect_request("/ws/2/release/6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9").respond_with_data(data)  # type: ignore
    client = Client(
        httpserver.url_for("/ws/2/release/6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
    )
    release = client.lookup_release("6c1adf00-edaf-4fe0-9d57-8dc5da90a4a9")
    assert release["title"] == "amo"
