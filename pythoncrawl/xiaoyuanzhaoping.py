#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
import pymongo
import MongoDBConn
import  random

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

def insertDatas(url,random,company_name,job_name,job_time,keyword,salary,dizi,edu,experience,yaoqiu,youxiang,desc,dianhua,renshu,lianxiren,fuli):
    global collection
    datas={"job_url":url,"company_name":company_name,"_fid":random,"job_name":job_name,"tag":keyword,"catch_time":job_time,"salary":salary,"job_location":dizi,"major":"None","edu":edu,"exp":experience,"linman":lianxiren,"job_req":yaoqiu,"contact_email":youxiang,"job_desc":desc,"attraction":fuli,"mark":"1","contact_phone":dianhua,"hire_num":renshu,"company_url":"None"}
    collection.insert(datas)


dbconn = MongoDBConn.DBConn()
conn = None
crawl_users = None
dbconn.connect()
conn = dbconn.getConn()
db_auth = conn.job_zhilian
collection=db_auth.whole

first_url = "http://xiaoyuan.zhaopin.com/full/0/763_0_210500,160400,160000,160500,160200,300100,160100,160600_0_4_0_0_1_0"
first_html = urlopen(first_url)
first_bsobj = BeautifulSoup(first_html.read(),"lxml")
#print(first_bsobj)
url_links = first_bsobj.findAll("p",{"class":"searchResultJobName clearfix"})
print(url_links)
for a in range(1,5):
    print(a)
    if a==1:
        url_page = first_url
    else:
        if a==2:
            url_page = "http://xiaoyuan.zhaopin.com/full/0/763_0_210500,160400,160000,160500,160200,300100,160100,160600_0_4_0_0_2_0"
        else:
            url_page = "http://xiaoyuan.zhaopin.com/full/0/763_0_210500,160400,160000,160500,160200,300100,160100,160600_0_4_0_0_"+a+"_0"
    print(url_page)
    html = urlopen(url_page)
    bsobj = BeautifulSoup(html,"lxml")
    for b in range(1,29):
        print(b)
        base_url = bsobj.findAll("p",{"class":"searchResultJobName clearfix"})[b].a.attrs['href']
        renshu=bsobj.findAll("em",{"class":"searchResultJobPeopnum"})[b].get_text()
        print(renshu)
        print(base_url)
        base_html = urlopen(base_url)
        base_bsobj = BeautifulSoup(base_html,'lxml')
        company_wangzhi=base_bsobj.findAll("p",{"class":"c9 mt5"})[0].a.get_text()
        company_dizi=base_bsobj.findAll("div",{"class":"clearfix p20"})[0].find("p").get_text().strip()
        print(company_dizi)
        print(company_wangzhi)
        jobname1 = base_bsobj.findAll("h1",{"id":"JobName"})
        fuli="无"
        p = re.compile(r'\w*',re.L)
        jobname2 = p.sub("",str(jobname1))
        jobname3 = re.sub("=","",str(jobname2))
        jobname4 =re.sub("\"","",str(jobname3))
        jobname5= re.sub("\<","",str(jobname4))
        jobname6 = re.sub("\>","",str(jobname5))
        jobname7 = re.sub("\/","",str(jobname6))
        jobname8 =re.sub("\[","",str(jobname7))
        jobname9 = re.sub("\]","",str(jobname8))
        jobcompany = base_bsobj.find("li",{"id":"jobCompany"}).a.get_text()
        jobclass =re.sub("\.\.\.","",base_bsobj.find("li",{"class":"cJobDetailInforWd2"}).get_text())
        job_class = base_bsobj.findAll("li",{"class":"cJobDetailInforWd2 marb"})[2].get_text()
        job_publictime = base_bsobj.findAll("li",{"class":"cJobDetailInforWd2 marb"})[3].get_text()
        job_desc = base_bsobj.find("div",{"class":"j_cJob_Detail"}).div.p.get_text()
        yaoqiu,desc=zhiweiyaoqiu(job_desc.strip())
        phone_num=catch_number(job_desc.strip())
        email=catch_email(job_desc.strip())
        random_id=random.randint(0,5000)
        keyword=""
        salary="面议"
        lianxiren="无"
        edu="专科/本科/研究生"
        experience="一年以上"
        insertDatas(base_url,random_id,jobcompany,jobname9,job_publictime,keyword,salary,company_dizi,edu,experience,yaoqiu,email,desc,phone_num,renshu,lianxiren,fuli)
        print(job_desc)
        print(job_publictime)
        print(jobname9.strip())
        print(job_class)
        print(jobcompany)
        print(jobclass)
        #csvfilename = jobname9.strip()+":"+jobcompany
        #with open(csvfilename,"wt",newline="") as datacsv:
        #    writer=csv.writer(datacsv,dialect=("excel"))
         #   writer.writerow([jobname9.strip()])
          #  writer.writerow([jobcompany])
           # writer.writerow([job_publictime])
            #writer.writerow([job_class])
          # 3 writer.writerow([jobclass])
           # writer.writerow([job_desc])
           # datacsv.close()

