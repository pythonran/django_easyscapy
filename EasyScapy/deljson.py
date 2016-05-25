import urllib2,urllib
import json


def http_delete():
    header = {}
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header['Accept-Encoding'] = 'gzip, deflate, sdch'
    header['Accept-Language'] = 'zh-CN,zh;q=0.8'
    header['Cache-Control'] = 'no-cache'
    header['Connection'] = 'keep-alive'
    header[
        'Cookie'] = 'Hm_lvt_f8bdd88d72441a9ad0f8c82db3113a84=1449819861; Hm_lpvt_f8bdd88d72441a9ad0f8c82db3113a84=1449819967'
    header['Host'] = 'www.youdaili.net'
    header['Pragma'] = 'no-cache'
    header['Upgrade-Insecure-Requests'] = '1'
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

    url = 'http://127.0.0.1:8000/EasyScapy/pcapfiles/'
    values = {'id': 13}

    jdata = json.dumps(values)
    request = urllib2.Request(url,jdata,headers=header)

    request.get_method = lambda: 'DELETE'
    request = urllib2.urlopen(request)
    return request.read()


resp = http_delete()
print resp