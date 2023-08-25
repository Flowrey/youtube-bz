# Contributing Guide

## Getting Started

### Development Environment

Prerequisites:

- Python 3.9+
- [Poetry](https://python-poetry.org/)

Install the dependencies with `poetry install --with dev`

### Running tests

We uses [pytest](https://docs.pytest.org/en/7.4.x/) for tests.

Run tests with `poetry run -m pytest`.

### Formatting your code

We use [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to keep our code formated.

Format the code with:
```
poetry run -m black ./youtube_bz/ ./tests
poetry run -m isort ./youtube_bz/ ./tests --profile=black
```

## Commit Messages

We try to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) specification for our commit messages.
