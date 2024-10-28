import os
import sys
import unittest
from unittest.mock import patch
import uuid
from fastapi import HTTPException
from pymongo.errors import PyMongoError
import pytest

from app.models.user import User
from app.services.user_service import create_user, get_all_users

# Add the app directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


class TestUserService(unittest.TestCase):

    @patch('app.services.user_service.db')
    def test_create_user_success_with_uuid(self, mock_db):
        user = User(
            name="John Doe",
            email="john@example.com",
            investment_capital=1000.0)
        mock_uuid = "123e4567-e89b-12d3-a456-426614174000"

        with patch('uuid.uuid4', return_value=uuid.UUID(mock_uuid)):
            response = create_user(user)

        assert response["message"] == "User created successfully"
        assert response["user_id"] == mock_uuid

        mock_db.users.count_documents.return_value = 1
        assert mock_db.users.count_documents({"id": mock_uuid}) == 1

    @patch('app.services.user_service.db')
    def test_create_user_success_with_uuid_and_investment_capital_is_None(
        self,
        mock_db
    ):
        user = User(name="John Doe", email="john@example.com")
        mock_uuid = "123e4567-e89b-12d3-a456-426614174000"

        with patch('uuid.uuid4', return_value=uuid.UUID(mock_uuid)):
            response = create_user(user)

        assert response["message"] == "User created successfully"
        assert response["user_id"] == mock_uuid

        mock_db.users.count_documents.return_value = 1
        assert mock_db.users.count_documents({"id": mock_uuid}) == 1

    @patch('app.services.user_service.db')
    def test_create_user_pymongo_error(self, mock_db):
        user = User(
            name="John Doe",
            email="john@example.com",
            investment_capital=1000.0)
        mock_db.users.insert_one.side_effect = PyMongoError("Database error")

        with patch('uuid.uuid4', side_effect=PyMongoError("Unexpected error")):
            with pytest.raises(HTTPException) as exc_info:
                create_user(user)

        assert exc_info.value.status_code == 500
        assert "An error occurred while creating the user" in exc_info.value.detail

    @patch('app.services.user_service.db')
    def test_create_user_unexpected_error(self, mock_db):
        user = User(
            name="John Doe",
            email="john@example.com",
            investment_capital=1000.0
        )
        mock_db.users.insert_one.side_effect = Exception("Unexpected error")

        with pytest.raises(HTTPException) as exc_info:
            create_user(user)

        assert exc_info.value.status_code == 500
        assert "An unexpected error occurred" in exc_info.value.detail

    @patch('app.services.user_service.db')
    def test_get_all_users_success(self, mock_db):
        mock_db.users.find.return_value = [
            {
                "id": "1",
                "name": "User1",
                "email": "user1@example.com",
                "investment_capital": 1000.0
            },
            {
                "id": "2",
                "name": "User2",
                "email": "user2@example.com",
                "investment_capital": 2000.0
            }
        ]

        response = get_all_users()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["name"], "User1")
        self.assertEqual(response[1]["name"], "User2")
        mock_db.users.find.assert_called_once()

    @patch('app.services.user_service.db')
    def test_get_all_users_db_error(self, mock_db):
        mock_db.users.find.side_effect = PyMongoError("Database error")

        with self.assertRaises(HTTPException) as context:
            get_all_users()

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn(
            "An error occurred while fetching users",
            context.exception.detail
        )

    @patch('app.services.user_service.db')
    def test_get_all_users_unexpected_error(self, mock_db):
        mock_db.users.find.side_effect = Exception("Unexpected error")

        with self.assertRaises(HTTPException) as context:
            get_all_users()

        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("An unexpected error occurred", context.exception.detail)


if __name__ == '__main__':
    unittest.main()
