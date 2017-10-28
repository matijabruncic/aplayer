import hashlib
import os
import pafy
import subprocess
import time

import sys


def should_still_play():
    with open("/var/lib/aplayer/am_i_home", 'r') as f:
        file_contents = f.read()
        f.close()
        if file_contents.strip() == "1":
            return True
        return False


def play_a_song(url):
    video = pafy.new(url)

    bestAudioUrl = video.getbestaudio()._url
    if should_still_play() is False:
        print "I'm not home, We'll play a song another time"
        sys.exit()

    process = subprocess.Popen(["mplayer", bestAudioUrl], stdout=subprocess.PIPE, preexec_fn=os.setsid)
    while process.poll() is None:
        if should_still_play():
            time.sleep(.200)
        else:
            process.terminate()
            break


directory = "/var/lib/aplayer/videolinks/"
songNameHashed = hashlib.md5(sys.argv[1]).hexdigest()
fileName = directory + songNameHashed

with open(fileName, "r") as file:
    for line in file:
        play_a_song(line)
    file.close()
