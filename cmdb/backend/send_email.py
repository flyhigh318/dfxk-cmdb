# -*- coding: utf-8 -*-
# Author: Maksim.G
import smtplib
from smtplib import SMTP_SSL

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class SendMail(object):
    def __init__(self, user=None, password=None, host='smtp.gmail.com', port=None,
                 smtp_starttls=None, smtp_ssl=True, debuglevel=0,
                 smtp_skip_login=False, encoding="utf-8", oauth2_file=None,
                 soft_email_validation=True, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.kwargs = kwargs
        self.debuglevel = debuglevel

    def login(self):
        """
        Login to the SMTP server using password. `login` only needs to be manually run when the
        connection to the SMTP server was closed by the user.
        """
        # ssl登录
        smtp = SMTP_SSL(self.host)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(self.debuglevel)
        smtp.ehlo(self.host)
        smtp.login(self.user, self.password)
        return smtp

    def connection(self):
        return smtplib.SMTP_SSL if self.ssl else smtplib.SMTP

    def send_email(self,mail_to ,mail_title, mail_content, sender_mail=None):
        smtp = self.login()
        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_mail
        msg["To"] = mail_to
        smtp.sendmail(sender_mail, mail_to, msg.as_string())
        smtp.quit()

### not finish

def send_email():
    from email.mime.text import MIMEText
    from email.header import Header
    from smtplib import SMTP_SSL

    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '7697****@qq.com'
    # pwd为qq邮箱的授权码
    pwd = '****kenbb***'  ## xh**********bdc
    # 发件人的邮箱
    sender_qq_mail = '7697****@qq.com'
    # 收件人邮箱
    receiver = 'yiibai.com@gmail.com'

    # 邮件的正文内容
    mail_content = '你好，这是使用python登录qq邮箱发邮件的测试'
    # 邮件标题
    mail_title = 'Maxsu的邮件'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()


def send_file():
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '7697****@qq.com'
    # pwd为qq邮箱的授权码
    pwd = '*****mkenb****'  ##
    # 发件人的邮箱
    sender_qq_mail = '7697****@qq.com'
    # 收件人邮箱
    receiver = 'yiibai.com@gmail.com'

    # 邮件的正文内容
    mail_content = "你好，<p>这是使用python登录qq邮箱发送HTML格式邮件的测试：</p><p><a href='http://www.yiibai.com'>易百教程</a></p>"
    # 邮件标题
    mail_title = 'Maxsu的邮件'

    # 邮件正文内容
    msg = MIMEMultipart()
    # msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = Header("接收者测试", 'utf-8')  ## 接收者的别名

    # 邮件正文内容
    msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('attach.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="attach.txt"'
    msg.attach(att1)

    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open('yiibai.txt', 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="yiibai.txt"'
    msg.attach(att2)

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()



def send_html():
    from email.mime.text import MIMEText
    from email.header import Header
    from smtplib import SMTP_SSL

    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '7697****@qq.com'
    # pwd为qq邮箱的授权码
    pwd = '***bmke********'  ##
    # 发件人的邮箱
    sender_qq_mail = '7697****@qq.com'
    # 收件人邮箱
    receiver = 'yiibai.com@gmail.com'

    # 邮件的正文内容
    mail_content = "你好，<p>这是使用python登录qq邮箱发送HTML格式邮件的测试：</p><p><a href='http://www.yiibai.com'>易百教程</a></p>"
    # 邮件标题
    mail_title = 'Maxsu的邮件'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = Header("接收者测试", 'utf-8')  ## 接收者的别名

    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
