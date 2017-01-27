import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

src = "file.png"

def notify(week, send_from,send_to,smtp_server,smtp_port,smtp_password,is_tls):
    msg = MIMEMultipart(
        From=send_from,
        To=send_to,
        Subject="Untis plan update"
    )
    msg.attach(MIMEText("Untis plan was updated"))

    reader = open(src,"rb")
    msg.attach(MIMEApplication(
                reader.read(),
                Content_Disposition='attachment; filename="plan.png"',
                Name="plan.png"
            ))

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.ehlo()
    if(is_tls):
        smtp.starttls()
    smtp.login(send_from,smtp_password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    print(send_to + ' was notified with sucesss!')