from abc import ABC, abstractmethod
from typing import List, Dict
from app.models.fund import Fund


class FundRepository(ABC):
    @abstractmethod
    def create_fund(self, fund: Fund) -> str:
        pass

    @abstractmethod
    def get_fund(self, fund_id: str) -> Dict:
        pass

    @abstractmethod
    def list_funds(self) -> List[Dict]:
        pass
