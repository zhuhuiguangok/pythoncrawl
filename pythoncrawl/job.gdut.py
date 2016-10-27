#!/usr/bin/env python
# encoding: utf-8
import math
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
import MongoDBConn
import pymongo
import  random
from selenium import webdriver
def zhiweiyaoqiu(s):
    mingzhi=["任职要求","岗位要求","职责要求","职位要求","任职资格","能力要求","任职条件","胜任要求"]
    ss="无"
    desc="无"
    s=re.sub("：","",s)
    s=re.sub("岗位职责","",s)
    for a in mingzhi:
        if re.search(a,s.strip()):
            b=re.search(a,s.strip()).span()
            print(b)
            c=re.search(r'([\d]+)',str(b))
            d=int(c.group(1))+4
            s=s.strip()
            ss=s[d:]
            print(ss)
            desc=s[:int(c.group(1))-1]
        else:
            pass
    if ss=="无":
        desc=s
        print(desc)
    return ss,desc

def catch_number(s):
    p=re.compile('[\d]+', re.IGNORECASE)
    phone=re.findall(p,s)
    biaoji=1
    for cha in phone:
        if cha=="":
            biaoji=1
        else:
            biaoji=0
    if biaoji:
        biaoji=1
        return "无"
    else:
        biaoji=0
        return cha

def catch_email(s):
    p1=re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b",re.IGNORECASE)
    email2=re.findall(p1,s)
    email1=""
    for email1 in email2:
        if email1=="":
            return "无"
        else:
            return email1

def insertDatas(url,random,company_name,job_name,job_time,keyword,salary,dizi,edu,experience,yaoqiu,youxiang,desc,dianhua,renshu,lianxiren):
    global collection
    datas={"job_url":url,"company_name":company_name,"_fid":random,"job_name":job_name,"tag":keyword,"catch_time":job_time,"salary":salary,"job_location":dizi,"major":"None","edu":edu,"exp":experience,"linman":lianxiren,"job_req":yaoqiu,"contact_email":youxiang,"job_desc":desc,"attraction":fuli,"mark":"1","contact_phone":dianhua,"hire_num":renshu,"company_url":"None"}
    collection.insert(datas)

dbconn = MongoDBConn.DBConn()
conn = None
crawl_users = None
dbconn.connect()
conn = dbconn.getConn()
db_auth = conn.job_class_test
collection=db_auth.design

keyword=input("Enter you want to crawl")
#keyword=keyword.decode("utf-8")
url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list?keyword=%E8%AE%BE%E8%AE%A1"
html=urlopen(url)
bsobj=BeautifulSoup(html.read(),"lxml")
numpage=bsobj.find("span",{"class":"text-orange mg-rl-10"}).get_text()
numquzheng=int(numpage)/10
numpage=math.ceil(numquzheng)
print(numpage)
#driver=webdriver.Chrome()
for k in range(1,numpage+1):
    if k==1:
        #url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list?keyword="+keyword
        url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list?keyword=%E8%AE%BE%E8%AE%A1"
    else:
        url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list?keyword=%E8%AE%BE%E8%AE%A1"
    html = urlopen(url)
    bsobj = BeautifulSoup(html.read(),"lxml")
    url_links = bsobj.findAll("a",{"class":"job-block card mg-b-10"})
	#print(url_links)
#for url_link in url_links:
#url_link.get_text()
    for i in range(0,10):
        job_url_id = bsobj.findAll("a",{"class":"job-block card mg-b-10"})[i].attrs['href']
        publich_time=bsobj.find("div",{"class":"col-xs-2 job-time"}).get_text()
        print(publich_time)
        id_num=catch_number(str(job_url_id))
        print(id_num)
        job_url='http://job.gdut.edu.cn/unijob/index.php/web/Index/'+job_url_id
        job_html=urlopen(job_url)
        job_bsobj=BeautifulSoup(job_html.read(),"lxml")
        job_companys = bsobj.findAll("div",{"class":"col-xs-4 col-xs-offset-1 job-company"})
        company_name=job_companys[i].text.strip()
        experience=job_bsobj.findAll("span",{"class":"badge"})[2].get_text()
        job_name=job_bsobj.find("div",{"style":"border-bottom: 1px solid #ddd;padding-bottom: 20px;"}).h1.get_text()
        print(experience)
        fuli=job_bsobj.find("div",{"style":"border-bottom: 1px solid #ddd;padding-bottom: 20px;"}).p.get_text()
        print(fuli)
        job_edu= bsobj.findAll("div",{"class":"col-xs-3 job-edu"})
        xueli=job_edu[i].text.strip()
        job_salarys = bsobj.findAll("div",{"class":"col-xs-4 job-salary"})
        salary=job_salarys[i].text.strip()
        print(salary)
        desc_s = job_bsobj.find("div",{"class":"content"}).get_text().strip()
        desc=desc_s.replace(u'\xa0',u' ')
        yaoqiu,desc=zhiweiyaoqiu(desc)
        #print(yaoqiu)
        print(xueli)
        dizi=job_bsobj.findAll("span",{"class":"label label-info"})[2].parent.get_text().strip()
        dizi=re.sub("地址","",dizi)
        job_url='http://job.gdut.edu.cn/unijob/index.php/wx/Index/'+job_url_id
        driver=webdriver.Chrome()
        driver.get(job_url)
        #company_name=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[2]/ul/li/div[2]/div[1]/div").text
        renshu=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[1]/span").text
        renshu=catch_number(renshu)
        #renshu=re.sub("(","",str(renshu))
        #renshu=re.sub(")","",renshu)
        dianhua=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[3]").text
        #print(job_url)
        #fuli=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/span").text
        #print(fuli)
        print(dianhua)
        youxiang=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[3]/div[3]").text
        print(youxiang)
        lianxiren=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[1]/div[3]").text
        print(lianxiren)
        #job_html=urlopen(job_url)
		#job_bsobj=BeautifulSoup(job_html.read(),"lxml")
        #job_html=urlopen(job_url)
        #job_bsobj=BeautifulSoup(job_html.read(),"lxml")
        print(job_name)
        #command=None
        #compemail=None
        #phone_num=None
        #job_num=None
        #renshu=job_bsobj.find("div",{"class":"weui_cell_ft"}).get_text()
        #dianhua=job_bsobj.findAll("div",{"class":"weui_cell_ft"}).get_text()
        #print(dianhua)
        print(renshu)
        #dizi=job_bsobj.find("div",{"class":"item-subtitle badg"}).get_text()
        print(dizi)
		#print(com_url)
		#print(job_name)
		#print(experience)
		#print(desc)
		#print(address)
		#print(job_time)
        job_companys = bsobj.findAll("div",{"class":"col-xs-4 col-xs-offset-1 job-company"})
        companys=job_companys[i].text.strip()
        job_salarys = bsobj.findAll("div",{"class":"col-xs-4 job-salary"})
        salary=job_salarys[i].text.strip()
		#print(companys)
		#print(salary)
        job_edu= bsobj.findAll("div",{"class":"col-xs-3 job-edu"})
        edu=job_edu[i].text.strip()
        #job_third_lines = bsobj.findAll("div",{"class":"third-line"})
        #job_third_line=job_third_lines[i].text.strip()
		#print(edu)
		#print(job_third_line)
        insertDatas(job_url,id_num,company_name,job_name,publich_time,keyword,salary,dizi,edu,experience,yaoqiu.strip(),youxiang,desc.strip(),dianhua,renshu,lianxiren)
        print(job_name)
        #print(job_time)
        print(salary)
        #print(address)
        print(edu)
        print(experience)
        #print(command)
        #print(com_url)
        #print(compemail)
        #print(job_third_line)
        print(desc)
        #print(phone_num)
        #print(job_num)
        driver.close()
