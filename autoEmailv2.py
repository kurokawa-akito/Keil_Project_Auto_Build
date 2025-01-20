import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def attachFile(msg, file_path):
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename = {file_name}")
        msg.attach(part)
    except FileNotFoundError:
        print(f"File Not Found: {file_path}")
        raise


def sendEmailWithFiles(
    smtp_server, smtp_port, from_addr, to_addr, hex_file_path, log_file_path
):
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.ehlo()

        subject = "Python Email with Attachment"

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addr)
        msg["Subject"] = subject

        body = "mail contents"
        msg.attach(MIMEText(body, "plain"))

        # Attach files
        attachFile(msg, hex_file_path)
        attachFile(msg, log_file_path)

        status = smtp.sendmail(from_addr, to_addr, msg.as_string())
        if status == {}:
            print("mail send")
        else:
            print("mail send failed")
        smtp.quit()

    except Exception as e:
        print(f"mail send error: {e}")
        raise


def gitPullFailedEmail(smtp_server, smtp_port, from_addr, to_addr):
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.ehlo()

        subject = "git pull failed Email"

        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addr)
        msg["Subject"] = subject

        body = "This auto build script stopped running due to a git pull failure."
        msg.attach(MIMEText(body, "plain"))

        status = smtp.sendmail(from_addr, to_addr, msg.as_string())
        if status == {}:
            print("git pull failed mail has send")
        else:
            print("git pull failed mail has send failed")
        smtp.quit()

    except Exception as e:
        print(f"git pull failed mail sending error: {e}")
        raise
