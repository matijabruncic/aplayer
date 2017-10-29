import time
from threading import Thread

from threading import Thread

import am_i_home
import configurator
import song_manager
import stream_a_song
import video_links_fetcher

thread = Thread(target=configurator.run)
thread.start()

old_value = am_i_home.check()
while True:
    new_value = am_i_home.check()
    if new_value is False:
        time.sleep(1)
    elif new_value != old_value:
        song_name = song_manager.random_song_name()
        video_links_fetcher.fetch(song_name)
        print "You've just got home and I got a song for you: " + song_name
        stream_a_song.play(song_name)
    old_value = new_value