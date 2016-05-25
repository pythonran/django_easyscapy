import urllib
import urllib2
import json


def http_post():

    url = 'http://127.0.0.1:8000/EasyScapy/sniffer/'

    values = {'status':'stop'}

    jdata = json.dumps(values)
    #jdata = urllib.urlencode(values)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()


resp = http_post()
print resp