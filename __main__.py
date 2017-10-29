import time
from multiprocessing import Process

import am_i_home
import configurator
import song_manager
import stream_a_song
import video_links_fetcher

server = Process(target=configurator.run)
server.start()

old_value = am_i_home.check()
try:
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
except KeyboardInterrupt:
    server.terminate()
    server.join()