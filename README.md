# YouTubeBrainz

YoutubeBrainz allows you to find and download Youtube videos associated to an album on MusicBrainz.

![example](docs/assets/gettingstarted.gif)

![Tests](https://github.com/flowrey/youtube-bz/actions/workflows/tests.yml/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/youtube-bz.svg)](https://badge.fury.io/py/youtube-bz)
![Downloads](https://static.pepy.tech/badge/youtube-bz)


## Summary

  - [Getting Started](#getting-started)
  - [How to use](#how-to-use)
  - [Author](#author)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  
## Getting Started

### Installation

You can install `youtube-bz` directly from pip, it should install automatically all the dependencies
```
$ pip install youtube-bz
```

## How to use
Display help
```console
$ youtube-bz --help
```

You can search for a release with its [MBID](https://musicbrainz.org/doc/MusicBrainz_Identifier) on [MusicBrainz](https://musicbrainz.org/) or
with the command search for instance to search the album 'Hybrid Theory' of 'Linkin Park' you can run:

```console
$ youtube-bz search 'Hybrid Theory' --artist 'Linkin Park'
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ ID                                   ┃ Title         ┃ Artist      ┃ Score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 2a4174ab-f0b1-430e-b7e2-25c062b45573 │ Hybrid Theory │ Linkin Park │ 100   │
│ cce15358-9fa0-38b5-b143-c51ff7024b24 │ Hybrid Theory │ Linkin Park │ 100   │
└──────────────────────────────────────┴───────────────┴─────────────┴───────┘
```

And to download it just run:
```console
$ youtube-bz download 2a4174ab-f0b1-430e-b7e2-25c062b45573MBID
```

## Author
  
  - **Flowrey** - [Flowrey](https://github.com/Flowrey)
  
## License

This project is licensed under the [GPL-3.0](LICENSE)
GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for
details

## Acknowledgments

  - This project's structure has been greatly inspired by [pipx](https://github.com/pypa/pipx/)
