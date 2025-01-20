import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

smtp = smtplib.SMTP('email server ip or DNS', 25)
smtp.ehlo()

from_addr = 'sender email'
to_addr = 'receiver email'

subject = "Python Email with Attachment"
current_time = datetime.now().strftime("%Y-%m-%d_%H%M")

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

# mail content
body = "mail content"
msg.attach(MIMEText(body, 'plain'))

file_path = f"D:\\keilHex\\Release_{current_time}.hex"
file_name = os.path.basename(file_path)

try:
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {file_name}',
    )
    msg.attach(part)

except FileNotFoundError:
    print("file not found")
    raise

status = smtp.sendmail(from_addr, to_addr, msg.as_string())

if status == {}:
    print("mail success")
else:
    print("mail failed")

smtp.quit()
