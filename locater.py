import re
import json
import urllib.request
from urllib.error import HTTPError

URL = "https://api.findip.net/{}/?token={}"
APIKEY = "[YOUR API KEY]"
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)

def addLocation(proxy):
    try:
        response = urllib.request.urlopen(URL.format(proxy.ip, APIKEY))
        location = json.load(response)
        if location is not None:
            proxy.lat = location["location"]["latitude"]
            proxy.lng = location["location"]["longitude"]
    except HTTPError as err:
        print(err)
    return proxy