import hashlib
import os
import subprocess
import sys
import time

import pafy

import am_i_home


def play(song_name):
    def should_still_play():
        am_i_home.check()
        with open("/var/lib/aplayer/am_i_home", 'r') as f:
            file_contents = f.read()
            f.close()
            if file_contents.strip() == "True":
                return True
            return False

    def play_a_song(url):
        video = pafy.new(url)

        best_audio_url = video.getbestaudio()._url
        if should_still_play() is False:
            print "I'm not home any more, we'll play a song another time"
            return False

        process = subprocess.Popen(["cvlc", best_audio_url], stdout=subprocess.PIPE, preexec_fn=os.setsid)
        while process.poll() is None:
            if should_still_play():
                time.sleep(.200)
            else:
                process.terminate()
                return False
        if process.returncode is 0:
            raise IOError("Return code from cvlc is" + process.returncode, process.stderr.read())
        else:
            return False

    directory = "/var/lib/aplayer/videolinks/"
    song_name_hashed = hashlib.md5(song_name).hexdigest()
    file_name = directory + song_name_hashed

    with open(file_name, "r") as f:
        for line in f:
            try:
                play_a_song(line.strip())
                break
            except:
                print sys.exc_info()[0]
        f.close()
