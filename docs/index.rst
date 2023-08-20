YouTubeBrainz
=============

YoutubeBrainz allows you to find and download Youtube videos associated 
to an album on MusicBrainz.

Installation
============

Requirements
------------

Before you use YouTubeBrainz you need to get yourself ``ffmpeg`` installed.
In Debian-like systems you can get it like this:

.. code-block:: console
        
        $ sudo apt install ffmpeg


From PyPi
---------

Then you can get YoutubeBrainz from PyPi repository directly:

.. code-block:: console

        $ pip install youtube-bz

From source
-----------

You can also install YouTubeBrainz from sources.

First, get a copy of the repository:

.. code-block:: console

        $ https://github.com/Flowrey/youtube-bz.git

And then, you can install it with pip:

.. code-block:: console

        $ cd youtube-bz
        $ pip install -e .


Getting started
===============

To get you started we will fetch an album from a MusicBrainzID.

Find a MBID
-----------

In this exemple we will get the album "Hybrid Theory" from "Linkin Park".

YouTubeBrainz need to use the MIBD of a release to download it.

For instance in the following URL: 

.. code-block:: text

        https://musicbrainz.org/release/5fc6445c-05ce-34e7-ab31-63bf7d3a9f24

the MBID is ``5fc6445c-05ce-34e7-ab31-63bf7d3a9f24``.

Now that we have the MBID we can download the release thanks to YouTubeBrainz.

Download the Release
--------------------

Downloading the release is really straight forward:

.. code-block:: console

        $ youtube-bz download 5fc6445c-05ce-34e7-ab31-63bf7d3a9f24

Your download should start now and you will get the YouTube videos
associated to the MBID album.
