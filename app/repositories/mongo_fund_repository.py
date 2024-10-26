import uuid
from typing import List, Dict
from app.utils.constants import DataBaseError
from app.utils.database import connect_db
from app.models.fund import Fund
from pymongo.errors import PyMongoError
from fastapi import HTTPException
from app.repositories.fund_repository import FundRepository

db = connect_db()


class MongoFundRepository(FundRepository):
    def create_fund(self, fund: Fund) -> str:
        try:
            fund_id = str(uuid.uuid4())
            fund_dict = fund.dict()
            fund_dict["id"] = fund_id
            db.funds.insert_one(fund_dict)
            return fund_id
        except PyMongoError:
            raise HTTPException(
                status_code=500,
                detail=DataBaseError.ERROR_DB_CONNECTION
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred: " + str(e)
            )

    def get_fund(self, fund_id: str) -> Dict:
        try:
            fund = db.funds.find_one({"id": fund_id})
            if not fund:
                raise HTTPException(status_code=404, detail="Fund not found")
            fund["_id"] = str(fund["_id"])  # Convert ObjectId to string
            return fund
        except PyMongoError:
            raise HTTPException(
                status_code=500,
                detail=DataBaseError.ERROR_DB_CONNECTION
            )

    def list_funds(self) -> List[Dict]:
        try:
            funds = list(db.funds.find())
            for fund in funds:
                fund["_id"] = str(fund["_id"])  # Convert ObjectId to string
            return funds
        except PyMongoError:
            raise HTTPException(
                status_code=500,
                detail=DataBaseError.ERROR_DB_CONNECTION
            )
