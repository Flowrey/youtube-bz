# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Use poetry with pyproject.toml instead of old setup.py
- Add pyright stub
- Add black and pyright to github action
### Fixed
- Fix bug when requestion MusicBrainz without User-Agent heade

## [0.3.3] - 2022-05-31
### Changed
- Use pytube instead of youtube-dl to download videos

## [0.3.2] - 2022-05-24
### Fixed
- Bug when video render in youtube initial data was empty

## [0.3.1] - 2022-05-21
### Added
- Unittest and code coverage
### Fixed
- Remaining debug print

## [0.3.0] - 2022-04-16
### Added
- Asyncronous code execution 
- Levenshtein distance for string comparaison
- ujson to parse json
- aiohttp for asyncronous request

### Changed
- Refactoring of all code

[Unreleased]: https://github.com/flowrey/youtube-bz/releases/tag/v0.3.3...HEAD
[0.3.3]: https://github.com/flowrey/youtube-bz/releases/tag/v0.3.3
[0.3.2]: https://github.com/flowrey/youtube-bz/releases/tag/v0.3.2
[0.3.1]: https://github.com/flowrey/youtube-bz/releases/tag/v0.3.1
[0.3.0]: https://github.com/flowrey/youtube-bz/releases/tag/v0.3.0
