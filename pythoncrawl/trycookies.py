#!/usr/bin/env python
# encoding: utf-8
import json
import re
import urllib
import http.cookiejar
from bs4 import BeautifulSoup
import pymongo
import sys
from urllib.error import HTTPError,URLError
from urllib.request import urlopen

url="http://so.dajie.com/job/ajax/search/filter?jobsearch=0&pagereferer=blank&ajax=1&keyword=java&page=7&order=0&from=user&salary=&recruitType=&city=&positionIndustry=&positionFunction=&degree=&quality=&experience=&_CSRFToken="
headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cookie':'SO_COOKIE=266as6y/D72EgDLqF3H9WnvJnptbSZSohYjAl3moJrEydMb8bFZ3zvwnOShfmQoXDpooPGnzrdwphdrPAocd4kRlASpOWObs1kwz; DJ_UVID=MTQ3NDc5NDMxNDQ3ODI5MzU4; login_email=870460771%40qq.com; __utma=246965659.514791355.1476765221.1476765221.1476765221.1; __utmb=246965659.1.10.1476765221; __utmz=246965659.1476765221.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); DJ_RF=empty; DJ_EU=http%3A%2F%2Fjob.dajie.com%2Fsearch%2Fadvance; __login_tips=1; dj_cap=fa873cd67dc194185d9f27507209547f; USER_ACTION="request^A-^A-^Ardc:1|jobdetail:^A-"',
            'Host':'so.dajie.com',
            'Referer':'http://so.dajie.com/job/search?keyword=java&_CSRFToken=',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
}

data = None
values={'':''}
jdata = json.dumps(values)
req = urllib.request.Request(url,data,headers)
#req.add_header(headers)
#req.get_method = lambda:'PUT'
response = urllib.request.urlopen(req)
compressedData = response.read()
print(compressedData)
