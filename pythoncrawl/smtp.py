#!/usr/bin/env python
# encoding: utf-8

from email.mime.application import MIMEApplication
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 输入Email地址和口令:
content = input("Enter you want to send:")
from_addr ="test@uoffer.net"
password ="lce0000:"
# 输入收件人地址:
to_addr =input("Enter which you want to send mail to:")
# 输入SMTP服务器地址:
smtp_server = "smtp.mxhichina.com"
server = smtplib.SMTP(smtp_server,25) # SMTP协议默认端口是25
msg = MIMEMultipart()
#msg = MIMEText('<html><body><h1>Helloh1>' +'<p>send by <a href="http://www.python.org">Python</a>a>...</p>p>'+'body>html>', 'html', 'utf-8')
#发送页面
htmlimg_or_plain=input("DO you want to insert image into content? yes or no:")
msg['From'] = _format_addr('LCE 科技 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('合作邀请信', 'utf-8').encode()
if htmlimg_or_plain=="yes":
    print("OK choice")
    imagepath = input("Enter your image path")
    msg.attach(MIMEText('<html><body><h1>%s</h1>'%content+'<p><img src="%s"></img></p>'%imagepath+'</body></html>', 'html', 'utf-8'))
else:
    msg.attach(MIMEText('%s'%content,'plain','utf-8'))
attach_decsion = input("do you want to attach a file?yes or no:")
# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
if attach_decsion=="yes":
    attach_type = input("attach-filetype? img or other:")
    filepath = input("Enter your filepath:")
    filename_1 =input("Enter your filename")
    if attach_type=="img":
        with open(filepath, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('image', 'png', filename='%s'%filename_1)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename='%s'%filename_1)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
    else:
        with open(filepath, "rb") as fil:
            msg.attach(MIMEApplication(fil.read(),Content_Disposition='attachment; filename="%s"' % basename(filename)))
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
