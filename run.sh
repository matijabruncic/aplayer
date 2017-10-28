#!/usr/bin/env bash

songName=$(python randomSongNameGenerator.py)
echo $songName
python videoLinksFetcher.py "$songName"
python streamASong.py "$songName"