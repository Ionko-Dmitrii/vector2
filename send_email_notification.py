import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_notification(email, heading, html):
    addr_from = "backend.sunrise.test@gmail.com"
    addr_to = email
    password = "krwdwwhsloeadlhr"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = heading

    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True) #ОТЛАДКА (ПОСТАВИТЬ TRUE)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
