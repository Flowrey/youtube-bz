from pathlib import Path

import nox  # type: ignore


@nox.session
def tests(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("-e", ".", "pytest", "pytest-cov", "pytest-httpserver")
    session.run("pytest", "--cov=youtube_bz", "--cov-report=", "tests")
    session.notify("cover")


@nox.session
def cover(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=95")
    session.run("coverage", "lcov")
    session.run("coverage", "erase")


@nox.session
def lint(session):
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("black", "isort", "pyright", "mypy")
    files = ["youtube_bz", "tests"] + [str(p) for p in Path(".").glob("*.py")]
    session.run("black", "--check", *files)
    session.run("isort", "--check", "--profile=black", *files)
    session.run("mypy", "--install-types", "--check-untyped-defs", *files)
