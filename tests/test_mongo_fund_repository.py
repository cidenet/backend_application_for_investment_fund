import unittest
from unittest.mock import patch, MagicMock
import uuid

import pytest
from app.models.fund import Fund
from app.repositories.mongo_fund_repository import MongoFundRepository
from fastapi import HTTPException
from pymongo.errors import PyMongoError

from app.utils.constants import DataBaseError


class TestMongoFundRepository(unittest.TestCase):

    @patch('app.repositories.mongo_fund_repository.db')
    def setUp(self, mock_db):
        self.mock_db = mock_db
        self.repository = MongoFundRepository()

    @patch('app.repositories.mongo_fund_repository.uuid.uuid4')
    def test_create_fund_success(self, mock_uuid):
        mock_uuid.return_value = uuid.UUID('12345678123456781234567812345678')
        fund = Fund(
            name="Test Fund",
            minimum_investment_amount=10000,
            category="FPV"
        )
        fund_id = self.repository.create_fund(fund)
        self.assertEqual(fund_id, '12345678-1234-5678-1234-567812345678')

    @patch('app.repositories.mongo_fund_repository.db')
    def test_create_fund_pymongo_error(self, mock_db):
        mock_db.funds.insert_one.side_effect = PyMongoError(
            DataBaseError.ERROR_DB_CONNECTION
        )
        fund = Fund(
            name="Test Fund",
            minimum_investment_amount=10000,
            category="FPV"
        )
        with self.assertRaises(HTTPException) as context:
            self.repository.create_fund(fund)
        self.assertEqual(context.exception.status_code, 500)
        self.assertIn(DataBaseError.ERROR_DB_CONNECTION, context.exception.detail)

    @patch('app.repositories.mongo_fund_repository.db')
    def test_get_fund_success(self, mock_db):
        mock_db.funds.find_one.return_value = {
            "id": "1234",
            "name": "Test Fund",
            "_id": MagicMock()
        }
        fund = self.repository.get_fund("1234")
        self.assertEqual(fund["id"], "1234")
        self.assertIn("_id", fund)
        mock_db.funds.find_one.assert_called_once_with({"id": "1234"})

    @patch('app.repositories.mongo_fund_repository.db')
    def test_get_fund_not_found(self, mock_db):
        mock_db.funds.find_one.return_value = None
        with self.assertRaises(HTTPException) as context:
            self.repository.get_fund("1234")
        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Fund not found", context.exception.detail)

    @patch('app.repositories.mongo_fund_repository.db')
    def test_get_fund_PyMongoError(self, mock_db):
        mock_db.funds.find_one.side_effect = PyMongoError(
            DataBaseError.ERROR_DB_CONNECTION
        )
        with self.assertRaises(HTTPException) as context:
            self.repository.get_fund("1234")
        self.assertEqual(context.exception.status_code, 500)
        self.assertIn(DataBaseError.ERROR_DB_CONNECTION, context.exception.detail)

    @patch('app.repositories.mongo_fund_repository.db')
    def test_list_funds_success(self, mock_db):
        mock_db.funds.find.return_value = [
            {
                "id": "1234",
                "name": "Test Fund",
                "_id": MagicMock()
            }
        ]
        funds = self.repository.list_funds()
        self.assertEqual(len(funds), 1)
        self.assertEqual(funds[0]["id"], "1234")
        self.assertIn("_id", funds[0])
        mock_db.funds.find.assert_called_once()

    @patch('app.repositories.mongo_fund_repository.db')
    def test_list_funds_pymongo_error(self, mock_db):
        mock_db.funds.find.side_effect = PyMongoError(DataBaseError.ERROR_DB_CONNECTION)
        with self.assertRaises(HTTPException) as context:
            self.repository.list_funds()
        self.assertEqual(context.exception.status_code, 500)
        self.assertIn(DataBaseError.ERROR_DB_CONNECTION, context.exception.detail)

    @patch('app.repositories.mongo_fund_repository.db')
    def test_create_fund_unexpected_error_v2(self, mock_db):
        mock_db.funds.insert_one.side_effect = Exception("Unexpected error")
        fund = Fund(
            name="test",
            minimum_investment_amount=100000,
            category="FPV"
        )
        mock_db.funds.create_fund.side_effect = Exception()

        with pytest.raises(HTTPException) as exc_info:
            self.repository.create_fund(fund)

        assert exc_info.value.status_code == 500
        assert "Unexpected error" in exc_info.value.detail


if __name__ == '__main__':
    unittest.main()
