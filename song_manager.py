import csv
import os
import sys
import uuid
from random import randint

directory = "/etc/aplayer/"
file_name = directory + "songs"


def random_song_name():
    song_names = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                song_names.append(str(row[1]).strip() + " " + str(row[2]).strip())
            f.close()
    else:
        sys.exit('Missing configuration file \'' + file_name + '\'')

    random_index = randint(0, len(song_names) - 1)
    return song_names[random_index]


def get_all_songs():
    songs = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                songs.append({'id': row[0], 'artist': row[1], 'name': row[2]})
            f.close()
    else:
        sys.exit('Missing configuration file \'' + file_name + '\'')
    return songs


def delete_a_song(song_id):
    if os.path.exists(file_name):
        with open(file_name, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if not line.startswith(song_id):
                    f.write(line)
            f.truncate()
            f.close()


def insert_new_song(song):
    with open(file_name, "a+") as f:
        f.write(create_row_from_song(str(uuid.uuid4()), song['artist'], song['name']))
        f.close()
    return None


def create_row_from_song(id, artist, name):
    return id + "," + artist + "," + name + '\n'
