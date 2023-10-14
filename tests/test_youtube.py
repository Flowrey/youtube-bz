import pytest
from pytest_httpserver import HTTPServer

from youtube_bz.api.youtube import Client, get_initial_data
from youtube_bz.api.youtube.exceptions import FailedToParseIntialData


def test_raise_failed_to_parse_yt_initial_data():
    data = "non_initial_data_regex"
    with pytest.raises(FailedToParseIntialData):
        get_initial_data(data)


def test_get_initial_data(httpserver: HTTPServer):
    data = 'var ytInitialData = {"foo":"bar"};</script><script'
    httpserver.expect_request("/results").respond_with_data(data)  # type: ignore
    client = Client(httpserver.url_for("/results"))
    res = client.get_search_results("Bring Me The Horizon")
    init_data = get_initial_data(res)
    print(init_data)
    assert init_data == {"foo": "bar"}
