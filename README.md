# YouTubeBrainz

YoutubeBrainz allow you to find Youtube Videos associated to an Album on MusicBrainz.

This software use the Google API as well as MusicBrainZ API.

## Usage

In order to work you need to put your API Key in ./youtube_bz/api.py
```python
class YoutubeAPI:
  
    __api_key = "MY_API_KEY"
 ```

Finaly you can launch the software with the MBID of your album (see https://musicbrainz.org/doc/MusicBrainz_Identifier)
```
$ pip install -e .
$ ./bin/youtube_bz [MBID]
```

