#!/usr/bin/env python
# encoding: utf-8

import csv
from selenium import webdriver
import re
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://qiye.aliyun.com")
bsobj = BeautifulSoup(html,"lxml")
print(bsobj)
email_login="http://qiye.aliyun.com"
username1 = "test@uoffer.net"
password1 = "lce@000^"
driver=webdriver.Chrome()
driver.get(email_login)
time.sleep(2)
driver.find_element_by_name("_fm.l._0.a").clear()
#driver.find_element_by_name("_fm.l._0.a").click()
driver.find_element_by_name("_fm.l._0.a").send_keys("test@uoffer.net")
#driver.find_element_by_xpath("//*[@id='username']").clear()
#driver.find_element_by_xpath("//*[@id='username']").send_keys(username1)
#driver.find_element_by_xpath("//*[@id='password_wrap']/input").clear()
#driver.find_element_by_xpath("//*[@id='password_wrap']/input").send_keys(password1)
#driver.find_element_by_xpath("//*[@id='login_submit_btn']").click()
