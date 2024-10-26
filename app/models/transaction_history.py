# transaction_history.py
from pydantic import BaseModel
from datetime import datetime


class TransactionHistory(BaseModel):
    id: str = None
    subscription_id: str
    action: str  # "created" or "cancelled"
    notification_channel: str = None  # This field will be ignored by the database
    timestamp: datetime = None
