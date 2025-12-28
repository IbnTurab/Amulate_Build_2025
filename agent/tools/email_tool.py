# tools/email_tool.py
import smtplib
from email.mime.text import MIMEText
import os

class EmailTool:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASS")
        self.from_addr = os.getenv("EMAIL_FROM")

    def send(self, to: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to
        with smtplib.SMTP(self.smtp_host) as server:
            if self.smtp_user and self.smtp_pass:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.from_addr, [to], msg.as_string())
        return {"to": to, "subject": subject, "status": "sent"}