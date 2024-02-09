from pathlib import Path

import nox  # type: ignore

PYTHON_ALL_VERSIONS = ["3.12", "3.11", "3.10", "3.9", "3.8"]
PYTHON_DEFAULT_VERSION = "3.12"
LINT_DEPENDENCIES = ["black", "isort", "mypy"]
DEV_DEPENDENCIES = ["pytest", "pytest-cov", "pytest-httpserver"]

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("-e", ".", *DEV_DEPENDENCIES)
    session.run("pytest", "--cov=youtube_bz", "--cov-report=", "tests")
    session.notify("cover")


@nox.session
def cover(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=95")
    session.run("coverage", "lcov")
    session.run("coverage", "erase")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install(*LINT_DEPENDENCIES)
    files = ["src/youtube_bz", "tests"] + [str(p) for p in Path(".").glob("*.py")]
    session.run("black", "--check", *files)
    session.run("isort", "--check", "--profile=black", *files)
    session.run("mypy", "--install-types", "--check-untyped-defs", *files)


@nox.session(python=PYTHON_ALL_VERSIONS)
def develop(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install(*DEV_DEPENDENCIES)
    session.install("-e", ".")
