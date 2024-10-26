# tests/test_fund_route.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from app.repositories.fund_repository import FundRepository
from app.services.fund_service import FundService

client = TestClient(app)


# Configurar un repositorio simulado
@pytest.fixture
def mock_repository():
    return MagicMock(spec=FundRepository)

# Parchear el servicio para que use el repositorio simulado
@pytest.fixture(autouse=True)
def patch_fund_service(mock_repository):
    with patch('app.routers.fund.fund_service', new=FundService(repository=mock_repository)):
        yield

def test_create_fund(mock_repository):
    # Mock the behavior of the repository to return a specific fund when a new fund is created
    mock_repository.create_fund.return_value = "1"
    mock_repository.get_fund.return_value = {
        "id": "1",
        "name": "test jdiaz",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    }

    response = client.post("/funds/", json={
        "name": "test jdiaz",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    })

    assert response.status_code == 200

def test_get_fund(mock_repository):
    fund_id = "1"
    mock_repository.get_fund.return_value = {
        "id": fund_id,
        "name": "test jdiaz",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    }
    response = client.get(f"/funds/{fund_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": fund_id,
        "name": "test jdiaz",
        "minimum_investment_amount": 100000,
        "category": "FPV"
    }
    mock_repository.get_fund.assert_called_once_with(fund_id)

def test_list_funds(mock_repository):
    mock_repository.list_funds.return_value = [
        {
            "id": "1",
            "name": "test jdiaz",
            "minimum_investment_amount": 100000,
            "category": "FPV"
        }
    ]

    response = client.get("/funds/")

    assert response.status_code == 200
    expected_response = [
        {
            "id": "1",
            "name": "test jdiaz",
            "minimum_investment_amount": 100000,
            "category": "FPV"
        }
    ]
    assert response.json() == expected_response
    mock_repository.list_funds.assert_called_once()

def test_list_funds_empty(mock_repository):
    mock_repository.list_funds.return_value = []
    response = client.get("/funds/")
    assert response.status_code == 200
    assert response.json() == []
