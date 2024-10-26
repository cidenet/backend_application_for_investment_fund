# notification_base.py
from abc import ABC, abstractmethod


class NotificationBase(ABC):
    @abstractmethod
    def send_notification(self, to: str, subject: str, body: str):
        pass
