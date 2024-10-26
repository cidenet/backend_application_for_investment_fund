from fastapi import HTTPException
from pymongo.errors import PyMongoError

from app.models.fund import Fund
from app.repositories.fund_repository import FundRepository
from app.utils.constants import DataBaseError, FundStatus, FundSuccessMessage


class FundService:
    def __init__(self, repository: FundRepository):
        self.repository = repository

    def create_fund(self, fund: Fund):
        try:
            if "status" not in fund.dict() or not fund.status:
                fund.status = FundStatus.ACTIVE
            fund_id = self.repository.create_fund(fund)
            response = {
                "message": FundSuccessMessage.SUCCESS_FUND_CREATED,
                "fund_id": fund_id
            }
            return response

        except PyMongoError:
            raise HTTPException(
                status_code=500,
                detail=DataBaseError.ERROR_DB_CONNECTION
            )
        except HTTPException as e:
            raise e

    def get_fund(self, fund_id: str):
        try:
            return self.repository.get_fund(fund_id)
        except HTTPException as e:
            raise e

    def list_funds(self):
        try:
            return self.repository.list_funds()
        except HTTPException as e:
            raise e
