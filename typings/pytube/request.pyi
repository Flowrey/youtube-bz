"""
This type stub file was generated by pyright.
"""

from functools import lru_cache

"""Implements a simple wrapper around urlopen."""
logger = ...
default_range_size = ...

def get(url, extra_headers=..., timeout=...):  # -> _UrlopenRet:
    """Send an http GET request.

    :param str url:
        The URL to perform the GET request for.
    :param dict extra_headers:
        Extra headers to add to the request
    :rtype: str
    :returns:
        UTF-8 encoded string of response
    """
    ...

def post(url, extra_headers=..., data=..., timeout=...):  # -> _UrlopenRet:
    """Send an http POST request.

    :param str url:
        The URL to perform the POST request for.
    :param dict extra_headers:
        Extra headers to add to the request
    :param dict data:
        The data to send on the POST request
    :rtype: str
    :returns:
        UTF-8 encoded string of response
    """
    ...

def seq_stream(
    url, timeout=..., max_retries=...
):  # -> Generator[_UrlopenRet, Unknown, None]:
    """Read the response in sequence.
    :param str url: The URL to perform the GET request for.
    :rtype: Iterable[bytes]
    """
    ...

def stream(url, timeout=..., max_retries=...):  # -> Generator[_UrlopenRet, Any, None]:
    """Read the response in chunks.
    :param str url: The URL to perform the GET request for.
    :rtype: Iterable[bytes]
    """
    ...

@lru_cache()
def filesize(url):  # -> int:
    """Fetch size in bytes of file at given URL

    :param str url: The URL to get the size of
    :returns: int: size in bytes of remote file
    """
    ...

@lru_cache()
def seq_filesize(url):  # -> int:
    """Fetch size in bytes of file at given URL from sequential requests

    :param str url: The URL to get the size of
    :returns: int: size in bytes of remote file
    """
    ...

def head(url):  # -> dict[_UrlopenRet, _UrlopenRet]:
    """Fetch headers returned http GET request.

    :param str url:
        The URL to perform the GET request for.
    :rtype: dict
    :returns:
        dictionary of lowercase headers
    """
    ...
