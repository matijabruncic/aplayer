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

pip install pafy