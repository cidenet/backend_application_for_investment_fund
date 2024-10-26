
# subscription.py
from pydantic import BaseModel


class Subscription(BaseModel):
    id: str = None
    status: str  # active or cancelled
    # This field will be ignored by the database
    subscription_notification_channel: str = None
    # Relationship
    user_id: str
    fund_id: str
