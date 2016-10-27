#!/usr/bin/env python
# encoding: utf-8
import math
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
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
    p=re.compile('[0-9][0-9][0-9][\d]+', re.IGNORECASE)
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

def insertDatas(from_site,detail_url,company_name,_fid,job_class,job_group,needs,post_time,catch_time,job_name,job_desc,job_req,major,attraction,advantage,location,edu,exp,contact,contact_phone,contact_email,contact_qq,contact_wechat,company_url,company_desc,mark):
    global collection
    datas={"from_site":from_site,
           "detail_url":detail_url,
           "company_name":company_name,
           "_fid":_fid,
           "job_class":job_class,
           "job_group":job_group,
           "needs":needs,
           "post_time":post_time,
           "catch_time":catch_time,
           "job_name":job_name,
           "job_desc":job_desc,
           "job_req":job_req,
           "major":major,
           "attraction":attraction,
           "advantage":advantage,
           "edu":edu,
           "exp":experience,
           "location":location,
           "contact":contact,
           "contact_phone":contact_phone,
           "contact_email":contact_email,
           "contact_qq":contact_qq,
           "contact_wechat":contact_wechat,
           " company_url":company_url,
           "company_desc":company_desc,
           "mark":mark}
    collection.insert(datas)

def get_json(url):
    detail_wx_html = urlopen(url)
    #str_info = detail_wx_html.read()
    str_info = detail_wx_html.read().decode('unicode-escape')
    str_info=re.sub("(?isu)<[^>]+>","" "",str_info).strip()
    #json_abc=json.loads(str_info)
    print(type(str_info))
    #json_abc=json.loads(str_info)
    print(str_info)
    decoded = json.loads(str_info,strict=False)
    print(decoded['contact'])
    #print(decoded)
    str_info[1:len(str_info)-1]
    clean_info = re.split(r',',str_info[1:len(str_info)-1])
    list_info=[]
    flag=0
    for flag in range(0,len(clean_info)-1):
        list_info.append(clean_info[flag])
        flag=flag+2

    for item in list_info:
        pass
        #print(item)
    #json_test=json.dumps(list_info)
    #print(json_test)

dbconn = MongoDBConn.DBConn()
conn = None
crawl_users = None
dbconn.connect()
conn = dbconn.getConn()
db_auth = conn.job_gdut
collection=db_auth.whole

#keyword=input("Enter you want to crawl")
#keyword=keyword.decode("utf-8")
url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list"
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
        url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list"
    else:
        url="http://job.gdut.edu.cn/unijob/index.php/web/Index/job-list?"+"p="+str(k)
    html = urlopen(url)
    bsobj = BeautifulSoup(html.read(),"lxml")
    url_links = bsobj.findAll("a",{"class":"job-block card mg-b-10"})
	#print(url_links)
#for url_link in url_links:
#url_link.get_text()
    for i in range(0,10):
        job_url_id = bsobj.findAll("a",{"class":"job-block card mg-b-10"})[i].attrs['href']
        print(job_url_id)
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
        job_id=catch_number(job_url_id)
        job_url=wx_detail_url_base='http://job.gdut.edu.cn/unijob/index.php/wx/jobs/detail?jid='+job_id + '&referer=http://job.gdut.edu.cn/unijob/index.php/wx/index/job-detail.html/id='+job_id
        #get_json(job_url)
        detail_wx_html = urlopen(job_url)
        str_info = detail_wx_html.read().decode('unicode-escape')
        str_info=re.sub("(?isu)<[^>]+>","" "",str_info).strip()
        decoded = json.loads(str_info,strict=False)
        contact=decoded['contact']
        experience_cn=decoded['experience_cn']
        addtime=decoded['addtime']
        jobs_name=decoded['jobs_name']
        education_cn=decoded['education_cn']
        contents=decoded['contents']
        yaoqiu,desc=zhiweiyaoqiu(contents)
        companyname=decoded['companyname']
        email=decoded['email']
        company_id=decoded['company_id']
        company_url="http://job.gdut.edu.cn/unijob/index.php/web/Index/company-info?id="+company_id
        sex_cn=decoded['sex_cn']
        nature_cn=decoded['nature_cn']
        district_cn=decoded['district_cn']
        amount=decoded['amount']
        wage_cn=decoded['wage_cn']
        trade_cn=decoded['trade_cn']
        company_id=decoded['company_id']
        phone_number=decoded['telephone']
        id_num=decoded['id']
        scale_cn=decoded['scale_cn']
        address=decoded['address']
        catch_time=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        print(catch_time)
        print(address)
        print(address)
        print(contact)
        #driver=webdriver.Chrome()
        #driver.get(job_url)
        #company_name=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[2]/ul/li/div[2]/div[1]/div").text
        #renshu=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[1]/span").text
        #renshu=catch_number(renshu)
        #renshu=re.sub("(","",str(renshu))
        #renshu=re.sub(")","",renshu)
        #dianhua=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[3]").text
        #print(job_url)
        #fuli=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/span").text
        #print(fuli)
        #print(dianhua)
        #youxiang=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[3]/div[3]").text
        #print(youxiang)
        #lianxiren=driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[2]/div/div[4]/div[2]/div/div/div/div/div[1]/div[3]").text
        #print(lianxiren)
        #job_html=urlopen(job_url)
		#job_bsobj=BeautifulSoup(job_html.read(),"lxml")
        #job_html=urlopen(job_url)
        #job_bsobj=BeautifulSoup(job_html.read(),"lxml")
        #print(job_name)
        #command=None
        #compemail=None
        #phone_num=None
        #job_num=None
        #renshu=job_bsobj.find("div",{"class":"weui_cell_ft"}).get_text()
        #dianhua=job_bsobj.findAll("div",{"class":"weui_cell_ft"}).get_text()
        #print(dianhua)
        #print(renshu)
        #dizi=job_bsobj.find("div",{"class":"item-subtitle badg"}).get_text()
        #print(dizi)
		#print(com_url)
		#print(job_name)
		#print(experience)
		#print(desc)
		#print(address)
		#print(job_time)
        #job_companys = bsobj.findAll("div",{"class":"col-xs-4 col-xs-offset-1 job-company"})
        #companys=job_companys[i].text.strip()
        #job_salarys = bsobj.findAll("div",{"class":"col-xs-4 job-salary"})
        #salary=job_salarys[i].text.strip()
		#print(companys)
		#print(salary)
        #job_edu= bsobj.findAll("div",{"class":"col-xs-3 job-edu"})
        #edu=job_edu[i].text.strip()
        #insertDatas(job_url,id_num,company_name,job_name,publich_time,keyword,salary,dizi,edu,experience,yaoqiu.strip(),youxiang,desc.strip(),dianhua,renshu,lianxiren)
        #print(job_name)
        #print(job_time)
        #print(salary)
        #print(address)
        #print(edu)
        #print(experience)
        #print(command)
        #print(com_url)
        #print(compemail)
        #print(job_third_line)
        #print(desc)
        #driver.close()
