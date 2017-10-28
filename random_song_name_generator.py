from random import randint
import os

import sys

directory = "/etc/aplayer/"


def generate():
    file_name = directory + "songs"
    song_names = []
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            for line in file:
                song_names.append(line.strip())
            file.close()
    else:
        sys.exit('Missing configuration file \'' + file_name + '\'')

    random_index = randint(0, len(song_names) - 1)
    return song_names[random_index]
