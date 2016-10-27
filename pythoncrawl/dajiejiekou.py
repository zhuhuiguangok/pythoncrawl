#!/usr/bin/env python
# encoding: utf-8
import bs4
import importlib
import sys
import urllib
import re
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
import http.cookiejar
import pymysql
import pymongo
import csv


login_url= "http://www.dajie.com/account/login"
keyword = input("Enter your searching keyword:")
job_name=input("Enter you want to crawl job_name:")
job_url = "http://so.dajie.com/job/search?ct=1475900688784&keyword="+keyword+"&filterPositionIndustry=&city=440100&filterPositionFunction=&salary=&degree=&experience=7&quality=&_CSRFToken=ZCgr7Zjsmw_OJqWHxO7lNOSTrXDmvO81He7XngNR"
#job_url =  "http://so.dajie.com/job/search?ct=1475904306580&keyword=java&filterPositionIndustry=&city=440100&filterPositionFunction=&salary=&degree=&experience=7&quality=&_CSRFToken=ZAIHwejNb86gF5jbJ46dIoyU6QmXdqSnSXSrejIc"
#print(type(job_url))
print(job_url)
filename = job_name+".txt"
values = {'text':'870460771@qq.com','password':'15626256939zhu'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
cookie =  http.cookiejar.MozillaCookieJar(filename)
handler =urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
request = urllib.request.Request(login_url,postdata,headers)
response = opener.open(request)
page= response.read().decode
#print(page)
cookie.save(ignore_discard=True,ignore_expires=True)
get_request  = urllib.request.Request(job_url,headers=headers)
get_response = opener.open(get_request)
text_html = get_response.read().decode()
sleep(1)
html = urlopen(job_url)
bsobj =BeautifulSoup(html.read(),"lxml")
print(bsobj)

