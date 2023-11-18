# Contributing Guide

## Getting Started

### Development Environment

Prerequisites:

- Python 3.9+
- [Nox](https://nox.thea.codes/en/stable/)

Install the dependencies with `nox -s develop`

### Running tests

We uses [pytest](https://docs.pytest.org/en/7.4.x/) for tests.

Run tests with `nox -s tests`.

### Formatting your code

We use [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to keep our code formated.

Format the code with:
```
black ./youtube_bz/ ./tests
isort ./youtube_bz/ ./tests --profile=black
```

You can check the formatting with nox
```
nox -s lint
```

## Commit Messages

We try to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) specification for our commit messages.
