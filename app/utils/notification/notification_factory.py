import os
from dotenv import load_dotenv

from .email_notification import EmailNotification
from .sms_notification import SMSNotification

load_dotenv()


class NotificationFactory:
    @staticmethod
    def get_notification(method: str):
        if method == "email":
            return EmailNotification(
                smtp_server=os.getenv("SMTP_SERVER"),
                smtp_port=int(os.getenv("SMTP_PORT")),
                username=os.getenv("SMTP_USERNAME"),
                password=os.getenv("SMTP_PASSWORD")
            )
        elif method == "sms":
            return SMSNotification()
        else:
            raise ValueError(f"Notification method {method} not supported")
