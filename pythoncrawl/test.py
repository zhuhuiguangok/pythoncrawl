#!/usr/bin/env python
# encoding: utf-8
import re
s="【岗位职责】： \n1、从事基于JAVA WEB的企业应用平台及系统研发工作。 \n2、依据项目要求和相关规范，完成系统的详细设计和相应文档的编写。 \n3、根据项目要求和编码规范，完成基于J2EE平台的相应编码任务。 \n4、根据项目要求，配合项目人员完成集成测试、系统测试和系统交付等工作。 \n\n【任职要求】： \n1、计算机或相关专业本科以上学历； \n2、具备较扎实的JAVA编程基本功，熟悉常用的数据结构, 算法知识； \n3、会使用Eclipse、MyEclipse，了解Java网络编程技术和多线程技术； \n4、了解Html,JavaScript,Jsp,CSS进行开发，了解AJAX,Jquery,Jstl等技术； \n5、具备较强的学习能力和良好的英语阅读能力，适应力强、能快速进入工作状态； \n6、具有较强的敬业精神，对工作认真、细致、负责；积极主动；具备较好的语言表达和沟通能力，较强的逻辑思维能力和团队合作精神，并能在一定压力下完成工作。"
mingzhi=["任职要求","岗位要求","职位要求"]
for a in mingzhi:
    if re.search(a,s):
        b=re.search(a,s).span()
        print(b)
        c=re.search(r'([\d]+)',str(b))
        d=int(c.group(1))+4
        ss=s[d:]
        print(ss)
    else:
        desc=s
        #print(desc)
