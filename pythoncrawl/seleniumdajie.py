#!/usr/bin/env python
# encoding: utf-8
import selenium
import MongoDBConn
from selenium import webdriver
import time
import re
import pymongo
import csv
import sys
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC


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


def put_into_mongo():
    #建立连接
    dbconn.connect()
    global conn
    conn = dbconn.getConn()
    #列出server_info信息
    print (conn.server_info())
    #列出全部数据库
    databases = conn.database_names()
    print (databases)
    #删除库和表
    dropTable()
    #插入数据
    insertDatas()
     #更新数据
    updateData()
     #查询数据
    queryData()
    #删除数据
    deleteData()
    #释放连接
    dbconn.close()

def insertDatas(url,random,company_name,job_name,job_time,keyword,salary,dizi,edu,experience,yaoqiu,youxiang,desc,dianhua,renshu,lianxiren):
    global collection
    datas={"job_url":url,"company_name":company_name,"_fid":random,"job_name":job_name,"tag":keyword,"catch_time":job_time,"salary":salary,"job_location":dizi,"major":"None","edu":edu,"exp":experience,"linman":lianxiren,"job_req":yaoqiu,"contact_email":youxiang,"job_desc":desc,"attraction":fuli,"mark":"1","contact_phone":dianhua,"hire_num":renshu,"company_url":"None"}
    collection.insert(datas)


def updateData():
    #只修改最后一条匹配到的数据
             #          第3个参数设置为True,没找到该数据就添加一条
            #           第4个参数设置为True,有多条记录就不更新
    crawl_users.update({'name':'steven1'},{'$set':{'realname':'测试1修改'}}, False,False)
#修改lifeba


def deleteData():
    crawl_users.remove({'name':'steven1'})

def queryData():
    #查询全部数据
    rows = crawl_users.find()
    printResult(rows)
    #查询一个数据
    print (crawl_users.find_one())
    #带条件查询
    printResult(crawl_users.find({'name':{'$gt':25}}))
    printResult(crawl_users.find({'name':'steven2'}))

def createTable():
    global crawl__users
    crawl_users = conn.crawl.users


def dropTable():
    global conn
    conn.drop_database("crawl")

def printResult(rows):
    for row in rows:
        for key in row.keys():#遍历字典
            print (row[key]+",") #加, 不换行打印
            print("")


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




def loginmethod():
    login_url = "http://www.dajie.com/account/login"
    driver  = webdriver.Chrome()
    driver.get(login_url)
    driver.find_element_by_xpath("//*[@id='login-email']").clear()
    driver.find_element_by_xpath("//*[@id='login-email']").send_keys("870460771@qq.com")
    driver.find_element_by_xpath("//*[@id='login-pwd']").clear()
    driver.find_element_by_xpath("//*[@id='login-pwd']").send_keys("15626256939zhu")
    driver.find_element_by_xpath("//*[@id='login-submit']/b").click()

dbconn = MongoDBConn.DBConn()
conn = None
crawl_users = None
dbconn.connect()
conn = dbconn.getConn()
db_auth = conn.job_dajie
collection=db_auth.whole
#createTable()
#db = conn.test
#users = db.users
#users = db['users']
keyword = input("Enter you want to crawl:")
driver_1 = webdriver.Chrome()
url = "http://so.dajie.com/job/search?ct=1475908555270&keyword="+keyword+"&filterPositionIndustry=&city=440100&filterPositionFunction=&salary=&degree=&experience=7&quality=&_CSRFToken="
driver_1.get(url)
#text = driver_1.find_element_by_xpath("//*[@id='J_suggestList']/li[1]/div/div/h3/a").text
page_len = driver_1.find_element_by_xpath("//*[@id='page-left']/div").get_attribute("lastpage")

#driver_1.find_element_by_xpath("")
for page_input in range(1,int(page_len)):
    if page_input!=1:
        driver_1.quit()
        driver_1=webdriver.Chrome()
        driver_1.get(url)
        driver_1.find_element_by_xpath("//*[@id='page-right']/input").send_keys(str(page_input))
        driver_1.find_element_by_xpath("//*[@id='J_loginDialog_school_1']/div/div/div/div[3]/span").click()
        time.sleep(2)
        driver_1.find_element_by_xpath("//*[@id='page-right']/span").click()
    for list_len in range(1,16):
        job_url = driver_1.find_element_by_xpath("//ul[@class='job-suggest-list']/li[%d]/div/div/h3/a" %list_len).get_attribute("href")
        xueli=driver_1.find_element_by_xpath("//*[@id='J_suggestList']/li[5]/div/p/span[4]").text
        driver_1.get(job_url)
        try:
            publish_time=driver_1.find_element_by_xpath("//*[@class='floatright']").text
        except NoSuchElementException:
            publish_time = driver_1.find_element_by_xpath("//*[@class='floatright']").text
        experience = driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[2]/div[2]/dl[2]/dd/span").text
        salary = driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[2]/div[2]/dl[1]/dd/span").text
        elements = driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[2]/div[2]/dl[1]/dd").text
        yaoqiu = driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[2]/div[2]/dl[2]/dd").text
        yaoqiu = yaoqiu.replace(experience,"")
        fuli = elements.replace(salary,"")
        job_dizi = driver_1.find_element_by_xpath("//*[@class='p-corp-detail-info']/dl[1]/dd").text
        job_desc = driver_1.find_element_by_xpath("//*[@id='jp_maskit']/p").text
        yaoqiu,desc=zhiweiyaoqiu(job_desc.strip())
        phone=catch_number(job_desc.strip())
        email3=catch_email(job_desc.strip())
        compname=driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[1]/div[1]/div/p/a").text
        compadrr=driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[1]/div[1]/div/ul/li[4]").text
        renshu=driver_1.find_element_by_xpath("//*[@id='jp-app-wrap']/div[2]/div[4]/dl[2]/dd/p").text
        insertDatas(compname,publish_time,salary,job_dizi.strip(),xueli,experience.strip(),yaoqiu,compadrr,email3,fuli,desc,phone,renshu)
        print(job_desc)
        print(job_dizi)
        print(yaoqiu.strip())
        print(fuli.strip())
        print(experience)
        print(salary)
        print(job_url,publish_time)
        print(page_input)
        #if page_input==1:
        if page_input==1:
            driver_1.get(url)
        else:
            driver_1.quit()
            driver_1 = webdriver.Chrome()
            driver_1.get(url)
            driver_1.find_element_by_xpath("//*[@id='page-right']/input").send_keys(str(page_input))
            driver_1.find_element_by_xpath("//*[@id='J_loginDialog_school_1']/div/div/div/div[3]/span").click()
            time.sleep(2)
            driver_1.find_element_by_xpath("//*[@id='page-right']/span").click()
        time.sleep(2)
        #else:
            #driver_1.get(url)
            #time.sleep(2)
            #for a in range(1,page_input):
            #    time.sleep(1)
            #    driver_1.find_element_by_xpath("//*[@class='paging']/a[12]").click()
            #    time.sleep(2)
            #    page_input = page_input-1
    #driver_1.get(url)
    #time.sleep(2)
    #for a in range(1,page_input):
    #    print(page_input)
    #    driver_1.find_element_by_xpath("//*[@class='paging']/a[12]").click()
    #    time.sleep(2)

print(page_len)
print(list_len)
dbconn.close()

#driver_1.find_element_by_xpath("//*[@id="page-right"]/input").send_keys("")
#driver_1.find_element_by_xpath("//*[@id='adse-con']/tbody/tr[1]/td[1]/input[1]").clear()
#driver_1.find_element_by_xpath("//*[@id='adse-con']/tbody/tr[1]/td[1]/input[1]").send_keys(keyword)
#driver_1.find_element_by_xpath("//*[@id='adse-con']/tbody/tr[4]/td[1]/select/option[4]").clear()
#driver_1.find_element_by_xpath("//*[@id='adse-con']/tbody/tr[4]/td[1]/select/option[4]").click()
#driver_1.find_element_by_xpath("//*[@id='city-input']").clear()
#driver_1.find_element_by_xpath("//*[@id='city-input']").send_keys("")
#sleep(1)
#driver_1.find_element_by_xpath("//*[@id='interactive-box-i-pluckpad1']/div/div/div[2]/div[2]/div/div[1]/ul/li[8]").click()
#sleep(1)
#driver_1.find_element_by_xpath("//*[@id='interactive-box-i-pluckpad1']/div/div/div[2]/div[2]/div/div[2]/ul/li[1]").click()
#sleep(1)
#driver_1.find_element_by_xpath("//*[@id='interactive-box-i-pluckpad1']/div/div/div[4]/button[1]").click()
