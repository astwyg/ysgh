import smtplib, traceback
from email.mime.text import MIMEText
from email.header import Header

from configs import mail as config
from log.logger import logger as log


def send_mail(subject, content, receiver):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(config.USER, 'utf-8')
    message['To'] = Header(receiver, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(config.HOST, 25)  # 25 为 SMTP 端口号
        smtpObj.login(config.USER, config.PASSWD)
        smtpObj.sendmail(config.USER, receiver, message.as_string())
        log.info("mail sent success.")
    except smtplib.SMTPException as e:
        log.error("mail sent failed")
        log.error(str(e))
        log.error(traceback.format_exc())