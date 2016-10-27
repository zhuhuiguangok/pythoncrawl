#!/usr/bin/env python
# encoding: utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
first_url ="http://www.horsehr.com/search/search_job_result.jsp?workcity=102100&posttype=100200,100300,100700&workyear=0&time=14"
first_html = urlopen(first_url)
bsobj = BeautifulSoup(first_html.read(),"lxml")
print(bsobj)
for a in range(1,20):
    url_link ="http://www.horsehr.com"+bsobj.findAll("li",{"class":"job search_bgc"})[a].a.attrs['href']
    print(url_link)
    html_page = urlopen(url_link)
    bsobj_page = BeautifulSoup(html_page,"lxml")
    #print(bsobj_page)
    jobname = bsobj_page.find("span",{"class":"job_word color_green l_h50 font24"}).h1.get_text()
    job_salary = bsobj_page.findAll("span",{"class":"column_2"})[1].get_text()
    print(job_salary)
    print(jobname)

