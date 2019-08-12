from readConfig import SendEmailConfig
import smtplib  # 发送邮件模块
from email.mime.text import MIMEText  # 定义邮件内容
from email.header import Header  # 定义邮件标题
from email.mime.multipart import MIMEMultipart  #用于传送附件
import os


class SendEmail:
    def __init__(self):
        self.smtpserver = SendEmailConfig().get_smtpserver()
        self.user = SendEmailConfig().get_user()
        self.password = SendEmailConfig().get_password()
        self.sender = SendEmailConfig().get_sender()
        self.receiver = SendEmailConfig().get_receiver()

    def send_mail(self, subject, path):
        # 发送邮件主题和内容
        if not subject:
            subject = 'Web Selenium 自动化测试报告'

        content = '<html><h1 style="color:blue">{}</h1></html>'.format(subject)

        # 构造附件内容,附件地址栏
        send_file = open(path, 'rb').read()

        att = MIMEText(send_file, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename="{}"'.format(os.path.split(path)[-1])

        # 构建发送与接收信息
        msgRoot = MIMEMultipart()
        msgRoot.attach(MIMEText(content, 'html', 'utf-8'))
        msgRoot['subject'] = subject
        msgRoot['From'] = self.sender
        msgRoot['To'] = ','.join(self.receiver)
        msgRoot.attach(att)

        # SSL协议端口号要使用465
        smtp = smtplib.SMTP_SSL(self.smtpserver, 465)

        # HELO 向服务器标识用户身份
        smtp.helo(self.smtpserver)
        # 服务器返回结果确认
        smtp.ehlo(self.smtpserver)
        # 登录邮箱服务器用户名和密码
        try:
            smtp.login(self.user, self.password)
        except Exception as e:
            print("登录失败！", e)

        try:
            print("Start send email...")
            smtp.sendmail(self.sender, self.receiver, msgRoot.as_string())
            smtp.quit()
            print("Send Sucessful！","\n")
        except Exception as e:
            print("Send Fail！")
            print(e)






