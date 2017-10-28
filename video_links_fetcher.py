import urllib2
import urllib
import json
import sys
import hashlib
import os


def fetch(song_name):
    url = "https://api.cognitive.microsoft.com/bing/v7.0/videos/search?"
    directory = "/var/lib/aplayer/videolinks/"
    
    def prepare_working_dir():
        if not os.path.exists(directory):
            os.makedirs(directory)

    prepare_working_dir()

    song_name_hashed = hashlib.md5(song_name).hexdigest()
    file_name = directory + song_name_hashed

    if os.path.exists(file_name):
        return

    query = urllib.urlencode({'q': song_name})
    req = urllib2.Request(url + query)
    req.add_header('Ocp-Apim-Subscription-Key', os.environ['MS_API_KEY'])
    response = urllib2.urlopen(req).read()
    data = json.loads(response)
    results = data['value']

    with open(file_name, 'w') as f:
        for result in results:
            url = result['contentUrl']
            f.write(url + "\n")
        f.close()
