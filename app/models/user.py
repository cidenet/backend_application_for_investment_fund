# user.py
from pydantic import BaseModel


class User(BaseModel):
    id: str = None
    name: str
    email: str
    investment_capital: float = None  # Field to store Colombian pesos
    phone_number: str = None
