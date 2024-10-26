import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .notification_base import NotificationBase


class EmailNotification(NotificationBase):
    """_summary_
    Send email notifications using SMTP
    Args:
        NotificationBase (_type_): _description_
    """
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_notification(self, to: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, to, text)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
