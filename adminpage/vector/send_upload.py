import mimetypes
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_upload():
    addr_from = "vectorobmennik@gmail.com"
    addr_to = "fakeoktx@gmail.com"
    password = "T3jbW46ryM"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Референс'

    body = ""
    msg.attach(MIMEText(body, 'plain'))

    filename = "reference.xlsx"
    ctype, encoding = mimetypes.guess_type(filename)
    maintype, subtype = ctype.split("/", 1)
    attachment = MIMEBase(maintype, subtype)
    with open(filename, "rb") as f:
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(False) #ОТЛАДКА (ПОСТАВИТЬ TRUE)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()