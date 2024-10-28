import pytest
from unittest.mock import MagicMock
from app.services.fund_service import FundService
from app.models.fund import Fund
from app.repositories.fund_repository import FundRepository
from fastapi import HTTPException
from app.utils.constants import FundSuccessMessage


@pytest.fixture
def mock_repository():
    return MagicMock(spec=FundRepository)


@pytest.fixture
def fund_service(mock_repository):
    return FundService(repository=mock_repository)


def test_create_fund(fund_service, mock_repository):
    fund = Fund(name="test", minimum_investment_amount=100000, category="FPV")
    mock_repository.create_fund.return_value = "1"

    response = fund_service.create_fund(fund)

    assert response == {
        "message": FundSuccessMessage.SUCCESS_FUND_CREATED,
        "fund_id": "1"
    }
    mock_repository.create_fund.assert_called_once_with(fund)


def test_get_fund(fund_service, mock_repository):
    fund_id = "1"
    mock_repository.get_fund.return_value = {
        "id": fund_id,
        "name": "test",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    }

    response = fund_service.get_fund(fund_id)

    assert response == {
        "id": fund_id,
        "name": "test",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    }
    mock_repository.get_fund.assert_called_once_with(fund_id)


def test_list_funds(fund_service, mock_repository):
    mock_repository.list_funds.return_value = [
        {
            "id": "1",
            "name": "test",
            "minimum_investment_amount": 100000,
            "category": "FPV"
        }
    ]

    response = fund_service.list_funds()

    assert response == [
        {
            "id": "1",
            "name": "test",
            "minimum_investment_amount": 100000,
            "category": "FPV"
        }
    ]
    mock_repository.list_funds.assert_called_once()


def test_create_fund_Http_exception_error_v3(fund_service, mock_repository):
    fund = Fund(
        name="test",
        minimum_investment_amount=100000,
        category="FPV"
    )
    mock_repository.create_fund.side_effect = HTTPException(
        status_code=400,
        detail="Bad Request"
    )

    with pytest.raises(HTTPException) as exc_info:
        fund_service.create_fund(fund)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bad Request"
    mock_repository.create_fund.assert_called_once_with(fund)
