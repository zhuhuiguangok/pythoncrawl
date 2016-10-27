#!/usr/bin/env python
# encoding: utf-8
import re
import csv
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import sys

def csv_init():
    idnum = "id"
    email_addr="邮箱"
    person = "联系人"
    companyname = "公司名字"
    position = "联系人职位"
    mark= "发邮件标识"
    frist_send_time="首次发送时间"
    total = "累计发送次数"
    last_send_time="上次发送时间"
    receiver_num="收到回复次数"
    frist_receive="首次回复时间"
    other="其他"
    data=[(idnum,email_addr,companyname,position,mark,frist_send_time,total,last_send_time,receiver_num,frist_receive,other)]
    with open("邮箱收发统计表.csv","wt") as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)





# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
                 # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                      # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            if n!=0:
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
            # 递归打印每一个子对象:
                print_info(part, indent + 1)
            else:
                pass
    else:
        # 邮件对象不是一个MIMEMultipart,
                # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码
            charset = guess_charset(msg)
            print(charset)
            if charset:
                content = content.decode(str(charset))
                #print(str(content))
            else:
                #content=decode_str(content)
                pass
            content = re.sub("(?isu)<[^>]+>","" "",content).strip()
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
             # 不是文本,作为附件处理:
             print('%sAttachment: %s' % ('  ' * indent, content_type))



def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
#邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：




#decode_header()返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素。上面的代码我们偷了个懒，只取了第一个元素。
#文本邮件的内容也是str，还需要检测编码，否则，非UTF-8编码的邮件都无法正常显示：
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
         # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


csv_init()
# 输入邮件地址, 口令和POP3服务器地址:
email ="test@uoffer.net"
password ="lce0000:"
pop3_server ="pop3.mxhichina.com"

# 连接到POP3服务器:
server = poplib.POP3(pop3_server,port=110)
# 可以打开或关闭调试信息:
# server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似['1 82923', '2 2184', ...]
print(mails)
print(resp,octets)
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = server.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)
print_info(msg)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()
