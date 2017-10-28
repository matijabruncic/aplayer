#!/usr/bin/env bash

if [ -z "$1" ]
then
    echo "Must specify user will run this app"
    exit 1
fi

install -d -g $1 -o $1 -m 0775 -v /var/lib/aplayer
if [ $? == "1" ]
then
    echo "Failed! Try using sudo.."
fi
install -d -g $1 -o $1 -m 0775 -v /etc/aplayer

touch /etc/aplayer/songs
chown $1:$1 /etc/aplayer/songs
echo "always look on the bright side of life life of brian" > /etc/aplayer/songs
touch /var/lib/aplayer/am_i_home
chown $1:$1 /var/lib/aplayer/am_i_home
echo "1" > /var/lib/aplayer/am_i_home

pip install pafy
pip install youtube-dl