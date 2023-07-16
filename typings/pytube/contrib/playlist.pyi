"""
This type stub file was generated by pyright.
"""

from collections.abc import Sequence
from datetime import date
from typing import Dict, Iterable, List, Optional, Union
from pytube import YouTube
from pytube.helpers import DeferredGeneratorList, cache

"""Module to download a complete playlist from a youtube channel."""
logger = ...
class Playlist(Sequence):
    """Load a YouTube playlist with URL"""
    def __init__(self, url: str, proxies: Optional[Dict[str, str]] = ...) -> None:
        ...
    
    @property
    def playlist_id(self): # -> str:
        """Get the playlist id.

        :rtype: str
        """
        ...
    
    @property
    def playlist_url(self): # -> str:
        """Get the base playlist url.

        :rtype: str
        """
        ...
    
    @property
    def html(self): # -> _UrlopenRet:
        """Get the playlist page html.

        :rtype: str
        """
        ...
    
    @property
    def ytcfg(self): # -> str:
        """Extract the ytcfg from the playlist page html.

        :rtype: dict
        """
        ...
    
    @property
    def initial_data(self): # -> str:
        """Extract the initial data from the playlist page html.

        :rtype: dict
        """
        ...
    
    @property
    def sidebar_info(self): # -> str:
        """Extract the sidebar info from the playlist page html.

        :rtype: dict
        """
        ...
    
    @property
    def yt_api_key(self): # -> str:
        """Extract the INNERTUBE_API_KEY from the playlist ytcfg.

        :rtype: str
        """
        ...
    
    def trimmed(self, video_id: str) -> Iterable[str]:
        """Retrieve a list of YouTube video URLs trimmed at the given video ID

        i.e. if the playlist has video IDs 1,2,3,4 calling trimmed(3) returns
        [1,2]
        :type video_id: str
            video ID to trim the returned list of playlist URLs at
        :rtype: List[str]
        :returns:
            List of video URLs from the playlist trimmed at the given ID
        """
        ...
    
    def url_generator(self): # -> Generator[str, Any, None]:
        """Generator that yields video URLs.

        :Yields: Video URLs
        """
        ...
    
    @property
    @cache
    def video_urls(self) -> DeferredGeneratorList:
        """Complete links of all the videos in playlist

        :rtype: List[str]
        :returns: List of video URLs
        """
        ...
    
    def videos_generator(self): # -> Generator[YouTube, Any, None]:
        ...
    
    @property
    def videos(self) -> Iterable[YouTube]:
        """Yields YouTube objects of videos in this playlist

        :rtype: List[YouTube]
        :returns: List of YouTube
        """
        ...
    
    def __getitem__(self, i: Union[slice, int]) -> Union[str, List[str]]:
        ...
    
    def __len__(self) -> int:
        ...
    
    def __repr__(self) -> str:
        ...
    
    @property
    @cache
    def last_updated(self) -> Optional[date]:
        """Extract the date that the playlist was last updated.

        For some playlists, this will be a specific date, which is returned as a datetime
        object. For other playlists, this is an estimate such as "1 week ago". Due to the
        fact that this value is returned as a string, pytube does a best-effort parsing
        where possible, and returns the raw string where it is not possible.

        :return: Date of last playlist update where possible, else the string provided
        :rtype: datetime.date
        """
        ...
    
    @property
    @cache
    def title(self) -> Optional[str]:
        """Extract playlist title

        :return: playlist title (name)
        :rtype: Optional[str]
        """
        ...
    
    @property
    def description(self) -> str:
        ...
    
    @property
    def length(self): # -> int:
        """Extract the number of videos in the playlist.

        :return: Playlist video count
        :rtype: int
        """
        ...
    
    @property
    def views(self): # -> int:
        """Extract view count for playlist.

        :return: Playlist view count
        :rtype: int
        """
        ...
    
    @property
    def owner(self): # -> str:
        """Extract the owner of the playlist.

        :return: Playlist owner name.
        :rtype: str
        """
        ...
    
    @property
    def owner_id(self): # -> str:
        """Extract the channel_id of the owner of the playlist.

        :return: Playlist owner's channel ID.
        :rtype: str
        """
        ...
    
    @property
    def owner_url(self): # -> str:
        """Create the channel url of the owner of the playlist.

        :return: Playlist owner's channel url.
        :rtype: str
        """
        ...
    


