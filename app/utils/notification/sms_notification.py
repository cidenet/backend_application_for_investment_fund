from .notification_base import NotificationBase
import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class SMSNotification(NotificationBase):
    """_summary_
    Send SMS notifications using AWS SNS
    Args:
        NotificationBase (_type_): _description_
    """
    def __init__(self):
        self.client = boto3.client(
            "sns",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )

    def send_notification(self, to: str, subject: str, body: str):
        # Implement the SMS sending logic here
        try:
            phone_number = str('+57' + to)
            # Send the SMS message
            response = self.client.publish(
                PhoneNumber=phone_number,
                Message=body
            )
            print(f"SMS sent to {to} with subject {subject}")
            return response
        except Exception as e:
            print("Error enviando SMS:", e)
            return None
