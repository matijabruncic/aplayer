import urllib2
import urllib
import json
import sys
import hashlib
import os


def fetch(song_name):
    url = "https://www.googleapis.com/customsearch/v1?"
    directory = "/var/lib/aplayer/videolinks/"
    
    def prepare_working_dir():
        if not os.path.exists(directory):
            os.makedirs(directory)

    prepare_working_dir()

    song_name_hashed = hashlib.md5(song_name).hexdigest()
    file_name = directory + song_name_hashed

    if os.path.exists(file_name):
        return

    key = os.environ["GOOGLE_API_KEY"]
    search_engine_id = os.environ["GOOGLE_SEARCH_ENGINE_ID"]
    query = urllib.urlencode({
		'q': song_name,
		'key': key,
		'cx': search_engine_id
		})
    req = urllib2.Request(url + query)
    response = urllib2.urlopen(req).read()
    data = json.loads(response)
    results = data['items']

    with open(file_name, 'w') as f:
        for result in results:
            url = result['formattedUrl']
            f.write(url + "\n")
        f.close()


