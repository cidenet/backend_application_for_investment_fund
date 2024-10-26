# fund.py
from pydantic import BaseModel


class Fund(BaseModel):
    id: str = None
    name: str
    minimum_investment_amount: float
    category: str
    status: str = None  # active or cancelled
