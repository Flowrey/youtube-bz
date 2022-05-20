# YouTubeBrainz

YoutubeBrainz allows you to find and download Youtube videos associated to an album on MusicBrainz.

[![PyPi version](https://img.shields.io/badge/pypi-0.3.0-blue)](https://pypi.org/project/youtube-bz/)
[![Python 3.9](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![GPL 3.0](https://img.shields.io/badge/license-GPL_3.0-blue.svg)](LICENSE.md)
[![Coverage Status](https://coveralls.io/repos/github/Flowrey/youtube-bz/badge.svg?branch=master)](https://coveralls.io/github/Flowrey/youtube-bz?branch=master)
![Coverage Status](https://github.com/flowrey/youtube-bz/actions/workflows/python-test.yml/badge.svg)


## Summary

  - [Getting Started](#getting-started)
  - [How to use](#how-to-use)
  - [Author](#author)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  
## Getting Started

### Installation

In order to extract audio from Youtube video, you will need to install ffmpeg:

Debian:
```
$ sudo apt install ffmpeg build-essential
```

Windows:
```
Download "ffmpeg-*-win64-gpl-*.*.zip" from: https://github.com/BtbN/FFmpeg-Builds/releases
Unzip it
Open the "bin" folder
Copy ffmpeg.exe, ffplay.exe and ffprobe.exe into your C:\Windows\ folder
```

Then you can install youtube-bz directly from pip, it should install automatically all the dependencies
```
$ sudo pip install youtube-bz
```

## How to use
Display help
```
$ youtube-bz --help
```

You can search for an album with its MBID (see https://musicbrainz.org/doc/MusicBrainz_Identifier)
```
$  youtube-bz MBID
```

## Author
  
  - **Flowrey** - [Flowrey](https://github.com/Flowrey)
  
## License

This project is licensed under the [GPL-3.0](LICENSE)
GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for
details

## Acknowledgments

  - This project's structure has been greatly inspired by youtube-dl
