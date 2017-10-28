import urllib2
import urllib
import json
import sys
import hashlib
import os

url = "https://api.cognitive.microsoft.com/bing/v7.0/videos/search?"
directory = "/var/lib/aplayer/videolinks/"


def prepareWorkingDir():
    if not os.path.exists(directory):
        os.makedirs(directory)


prepareWorkingDir()
if len(sys.argv) is 1:
    sys.exit('Missing mandatory parameter \'search string\'')

print sys.argv[1]
songNameHashed = hashlib.md5(sys.argv[1]).hexdigest()
fileName = directory + songNameHashed
print fileName

if os.path.exists(fileName):
    # with open(fileName, "r") as file:
    #     for line in file:
    #         print line.strip()
    #     file.close()
        sys.exit()

query = urllib.urlencode({'q': sys.argv[1]})
req = urllib2.Request(url + query)
req.add_header('Ocp-Apim-Subscription-Key', os.environ['MS_API_KEY'])
response = urllib2.urlopen(req).read()
data = json.loads(response)
results = data['value']

with open(fileName, 'w') as file:
    for result in results:
        url = result['contentUrl']
        file.write(url + "\n")
    file.close()
