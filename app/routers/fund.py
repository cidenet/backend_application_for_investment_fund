# fund_router.py
from fastapi import APIRouter
from app.models.fund import Fund
from app.repositories.mongo_fund_repository import MongoFundRepository
from app.services.fund_service import FundService

router = APIRouter()


# Create an instance of the repository and the service
repository = MongoFundRepository()
fund_service = FundService(repository=repository)


@router.post("/funds/")
def create_fund_endpoint(fund: Fund):
    return fund_service.create_fund(fund)


@router.get("/funds/{fund_id}")
def get_fund_endpoint(fund_id: str):
    return fund_service.get_fund(fund_id)


@router.get("/funds/")
def list_funds_endpoint():
    return fund_service.list_funds()
