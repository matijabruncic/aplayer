import time
import am_i_home
import random_song_name_generator
import stream_a_song
import video_links_fetcher

old_value = am_i_home.check()
while True:
    new_value = am_i_home.check()
    if new_value is False:
        time.sleep(1)
    elif new_value != old_value:
        song_name = random_song_name_generator.generate()
        video_links_fetcher.fetch(song_name)
        print "You've just got home and I got a song for you: " + song_name
        stream_a_song.play(song_name)
    old_value = new_value
