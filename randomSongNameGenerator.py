from random import randint
import os

import sys

directory = "/var/lib/aplayer/"

fileName = directory + "songNames"
songNames = []
if os.path.exists(fileName):
    with open(fileName, "r") as file:
        for line in file:
            songNames.append(line.strip())
        file.close()
else:
    sys.exit('Missing configuration file \'' + fileName + '\'')

randomIndex = randint(0, len(songNames) - 1)
print songNames[randomIndex]
