import mimetypes
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_code(email, code):
    addr_from = "vectorobmennik@gmail.com"
    addr_to = email
    password = "T3jbW46ryM"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Подтверждение почты'

    body = f"Код подтверждения: <b>{code}</b>"
    html = f"""\
    <html>
      <head></head>
      <body>
        <h1>Код подтверждения: <b>{code}</b></h1>
      </body>
    </html>
    """
    #msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))




    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True) #ОТЛАДКА (ПОСТАВИТЬ TRUE)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
