#coding=utf-8
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
def insert(cnx,cursor,table_name,insert_dict):
    param='';
    value='';
    if(isinstance(insert_dict,dict)):
        for key in insert_dict.keys():
            param=param+key+","
            value=value+insert_dict[key]+','
        param=param[:-1]
        value=value[:-1]
    sql="insert into %s (%s) values(%s)"%(table_name,param,value)
    cursor.execute(sql)
    id=cursor.lastrowid
    cnx.commit()
    return id



def sql_put_in_storage(post_time,mark,job_url,company_name,job_name,salary,exp_edu,attraction):
    list=[]
    data=(post_time,mark,job_url,company_name,job_name,salary,exp_edu,attraction)
    list.append(data)
    conn = pymysql.connect(host = 'local',port = 3306,user = 'root',passwd = 'root',charset = 'UTF8')
    cur = conn.cursor()
    cur.execute("START TRANSACTION;")
    #cur.execute("CREATE DATABASE indexdb;")
    cur.execute("USE indexdb;")
    cur.execute("CREATE TABLE index_c(index_java_id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,catch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,post_time VARCHAR(255),mark INT NOT NULL,job_url VARCHAR(255),company_name VARCHAR(100) character set utf8,job_name VARCHAR(255),salary VARCHAR(20),exp_edu VARCHAR(100),attraction TEXT)ENGINE=InnoDB;")
    #cur.execute("source /home/zhuhuiguang/index.sql")
    sql="insert into index_c(post_time,mark,job_url,company_name,job_name,salary,exp_edu,attraction)VALUE(%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(sql,list)
    cur.close()
    conn.commit()
    conn.close()

def getTitle(url):
    try:
        html = urlopne(url)
    except (HTTPError,URLError) as e:
        return None
    try:
        bsObj =Beautifulsoup(html.read())
        title = bsObj.body.h1 #
    except AttributeError as e:
        return None
    return title


def standard_message(url):
    standard_html = urlopen(url)
    standard_bsobj = BeautifulSoup(standard_html,'lxml')
    job_name =standard_bsobj.find("dt",{"class":"clearfix join_tc_icon"}).h1.get_text()
    #job_salary = standard_bsobj.findAll("dd",{"class":"job_request"}).find("p")[1].find("span")[1].get_text()
    job_name_cp = job_name.replace(" ","")
    job_company_cp=standard_bsobj.find("dt",{"class":"clearfix join_tc_icon"}).h1.div.get_text()
    job_salary_cp =standard_bsobj.find("dd",{"class":"job_request"}).p.findAll("span")[0].get_text()
    job_area_cp =standard_bsobj.find("dd",{"class":"job_request"}).p.findAll("span")[1].get_text()
    job_experience_cp = standard_bsobj.find("dd",{"class":"job_request"}).p.findAll("span")[2].get_text()
    job_eduback_cp =standard_bsobj.find("dd",{"class":"job_request"}).p.findAll("span")[3].get_text()
    job_time_cp =standard_bsobj.find("dd",{"class":"job_request"}).p.findAll("span")[4].get_text()
    job_tempt_cp =standard_bsobj.find("dd",{"class":"job_request"}).findAll("p")[1].get_text()
    job_desc_cp = standard_bsobj.find("dd",{"class":"job_bt"}).get_text()
    print(job_desc_cp)
    print(job_time_cp.strip())
    print(job_eduback_cp.strip())
    print(job_salary_cp.strip())
    print(job_company_cp.strip())
    print(job_name_cp.strip())
    print(job_area_cp.strip())
    print(job_tempt_cp.strip())
    csvfilename = job_company_cp.strip()
    csvfile = open(csvfilename,'wt')
    writer =csv.writer(csvfile,delimiter=',')
    csvfile.write('\n'.join(job_company_cp))
    csvfile.write('\n'.join(job_name_cp))
    csvfile.write('\n'.join(job_eduback_cp))
    csvfile.write('\n'.join(job_salary_cp))
    csvfile.write('\n'.join(job_area_cp))
    csvfile.write('\n'.join(job_tempt_cp))
    csvfile.write('\n'.join(job_experience_cp))
    csvfile.write('\n'.join(job_desc_cp))
    csvfile.write('\n'.join(job_time_cp))
    csvfile.close()

importlib.reload(sys)
start = time.clock()
filename = "cookie.txt"
values = {'username':'15626256939','password':'15626256939'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
cookie =  http.cookiejar.MozillaCookieJar(filename)
handler =urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
loginurl = 'https://passport.lagou.com/login/login.html?ts=1472888436922&serviceId=lagou&service=http%253A%252F%252Fwww.lagou.com%252F&action=login&signature=BD075A23AB039CB0867E1E9F14898602'
request = urllib.request.Request(loginurl,postdata,headers)
response = opener.open(request)
page= response.read().decode
cookie.save(ignore_discard=True,ignore_expires=True)
keysword=input("Enter you want to crawl")
javajoburl = "http://www.lagou.com/jobs/list_"+keysword+"?px=default&gj=%E5%BA%94%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F&city=%E5%B9%BF%E5%B7%9E#filterBox"
get_request  = urllib.request.Request(javajoburl,headers=headers)
get_response = opener.open(get_request)
html = get_response.read().decode()
bsobj = BeautifulSoup(html,'lxml')
mark =1
for a in range(0,15):
    link =bsobj.findAll("a",{"class":"position_link"})[a]
    if 'href' in link.attrs:
        completed_link ="http://"+re.sub('//','',str(link.attrs['href']))
        print(completed_link)
    publictime =bsobj.findAll("span",{"class":"format-time"})[a].get_text()
    experience = bsobj.findAll("div",{"class":"p_bot"})[a].find("div").get_text()
    jobname = bsobj.findAll("a",{"class":"position_link"})[a].find("h2").get_text()
    area =bsobj.findAll("span",{"class":"add"})[a].find("em").get_text()
    salary = bsobj.findAll("div",{"class":"p_bot"})[a].find("span").get_text()
    company_name  =bsobj.findAll("div",{"class":"company_name"})[a].find("a").get_text()
    tempt = bsobj.findAll("div",{"class":"list_item_bot"})[a].find("div").get_text()
    print(company_name.strip())
    #put_in_storage(publictime.strip(),mark,completed_link,company_name.strip(),jobname.strip(),salary.strip(),experience.strip(),tempt.strip())
    print(experience.strip())
    print(publictime.strip())
    print(salary.strip())
    print(area.strip())
    print(tempt.strip())
    print(jobname.strip())

for link in bsobj.findAll("a",{"class":"position_link"}):
    if 'href' in link.attrs:
        completed_link ="http://"+re.sub('//','',str(link.attrs['href']))
#        standard_message(completed_link)
        print(completed_link)
#哈哈
pagenum_total=bsobj.findAll("div,{"class":"span totalNum"}").span[1].text
pagelink  = bsobj.findAll("a",{"class":"page_no"})[2]
for page_number in range(1,pagenum_total):
    if page_number==1:
        pass
    else:
        page_newlink ="http:"+re.sub('2',str(page_number),str(pagelink.attrs['href']))
        print(page_newlink)
        basepage_request =urllib.request.Request(page_newlink)
        basepage_response = opener.open(basepage_request)
        new_html = basepage_response.read().decode()
        new_bsobj = BeautifulSoup(new_html,'lxml')
        for a in range(0,15):
            link =bsobj.findAll("a",{"class":"position_link"})[a]
            if 'href' in link.attrs:
                completed_link ="http://"+re.sub('//','',str(link.attrs['href']))
            publictime =new_bsobj.findAll("span",{"class":"format-time"})[a].get_text()
            experience = new_bsobj.findAll("div",{"class":"p_bot"})[a].find("div").get_text()
            jobname = new_bsobj.findAll("a",{"class":"position_link"})[a].find("h2").get_text()
            salary = new_bsobj.findAll("div",{"class":"p_bot"})[a].find("span").get_text()
            company_name  =new_bsobj.findAll("div",{"class":"company_name"})[a].find("a").get_text()
            tempt = new_bsobj.findAll("div",{"class":"list_item_bot"})[a].find("div").get_text()
            put_in_storage(publictime.strip(),mark,completed_link,company_name.strip(),jobname.strip(),salary.strip(),experience.strip(),tempt.strip())
        for new_link in new_bsobj.findAll("a",{"class":"position_link"}):
            if 'href' in new_link.attrs:
                completed_linkone = "http:"+str(new_link.attrs['href'])
                print(completed_linkone)


end =time.clock()
print("fetch:%f s"%(end-start))
