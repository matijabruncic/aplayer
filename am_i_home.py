import subprocess

import os

import datetime

import time

import sys

fileName = "/var/lib/aplayer/am_i_home"


def check():
    def am_i_home():
        with open("/var/lib/aplayer/am_i_home", 'r') as f:
            file_contents = f.read()
            f.close()
            if file_contents.strip() == "True":
                return True
            return False

    i_am_home = am_i_home()
    dig = subprocess.Popen(["dig", "+short", "android-6042c858a3b6712d"], stdout=subprocess.PIPE, preexec_fn=os.setsid)
    while dig.poll() is None:
        time.sleep(.50)
    if dig.returncode is not 0:
        sys.exit(1)
    out = dig.stdout.read().strip()
    if i_am_home is False:
        if len(out) > 0:
            print str(datetime.datetime.now().time()) + " - Dosao sam doma"
            i_am_home = True
    else:
        if len(out) is 0:
            print str(datetime.datetime.now().time()) + " - Nisam vise doma"
            i_am_home = False

    with open(fileName, 'w') as file:
        file.write(str(i_am_home))
        file.close()

    return i_am_home

