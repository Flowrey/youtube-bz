import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-bz",
    version="0.3.2",
    author="Flowrey",
    author_email="flowrey@laposte.net",
    description="YoutubeBrainz allow you to find and download Youtube Videos associated to an Album on MusicBrainz.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flowrey/youtube-bz",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/flowrey/youtube-bz/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['youtube-dl', 'aiohttp[speedups]', 'ujson', 'python-Levenshtein'],
    entry_points={
        'console_scripts': [
            'youtube-bz = youtube_bz:main',
        ],
    },
)
