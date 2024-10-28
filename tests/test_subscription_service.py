from datetime import datetime
import sys
import os
import unittest
from unittest.mock import patch
from fastapi import HTTPException
from pymongo.errors import PyMongoError
import pytest

from app.utils.constants import (
    DataBaseError,
    SuccessMessage,
    TransactionAction,
    SubscriptionError
)

from app.services.subscription_service import (
    create_subscription,
    cancel_subscription,
    get_user_transactions,
    list_subscriptions_with_users
)

from app.models.subscription import Subscription

# Add the app directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


class TestSubscriptionService(unittest.TestCase):

    @patch('app.services.subscription_service.db')
    def test_create_subscription_success(self, mock_db):
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 10000
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A",
            "minimum_investment_amount": 5000
        }

        mock_db.users.update_one.return_value = True
        mock_db.subscriptions.insert_one.return_value = None
        mock_db.subscriptions.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        response = create_subscription(subscription)

        self.assertEqual(response["detail"], SuccessMessage.SUCCESS_SUBSCRIPTION)
        self.assertIn("subscription_id", response)

    @patch('app.services.subscription_service.db')
    def test_create_subscription_pymongo_error_PyMongoError_Except(self, mock_db):
        subscription = Subscription(
            user_id="1",
            fund_id="fund123",
            amount=1000.0,
            status="active"
        )

        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 10000
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A",
            "minimum_investment_amount": 5000
        }

        mock_db.subscriptions.insert_one.side_effect = PyMongoError("Database error")
        mock_db.subscriptions.find_one.return_value = None

        with pytest.raises(HTTPException) as excinfo:
            create_subscription(subscription)

        assert excinfo.value.status_code == 500
        assert DataBaseError.ERROR_DB_CONNECTION in excinfo.value.detail
        mock_db.subscriptions.insert_one.assert_called_once()

    @patch('app.services.subscription_service.db')
    def test_create_subscription_error_capital_not_success(self, mock_db):
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 8000
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A",
            "minimum_investment_amount": 20000
        }

        mock_db.users.update_one.return_value = True
        mock_db.subscriptions.insert_one.return_value = None
        mock_db.subscriptions.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            str(SubscriptionError.ERROR_NO_AVAILABLE_BALANCE) + " Fund A"
        )

    @patch('app.services.subscription_service.db')
    def test_create_subscription_error_fund_minimum_investment_amount_is_none(
        self,
        mock_db
    ):
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 8000
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A"
        }

        mock_db.users.update_one.return_value = True
        mock_db.subscriptions.insert_one.return_value = None
        mock_db.subscriptions.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            SubscriptionError.ERROR_NO_MINIMUM_AMOUNT_TO_INVEST
        )

    @patch('app.services.subscription_service.db')
    def test_create_subscription_error_subscribtion_exists_with_fund_and_user(
        self,
        mock_db
    ):
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 8000
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A"
        }

        mock_db.users.update_one.return_value = True
        mock_db.subscriptions.insert_one.return_value = None
        mock_db.subscriptions.find_one.return_value = {
            "user_id": "user123",
            "fund_id": "fund123"
        }

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            SubscriptionError.ERROR_USER_ALREADY_SUBSCRIBED_TO_FUND
        )

    @patch('app.services.subscription_service.db')
    def test_create_subscription_user_not_exist(self, mock_db):
        mock_db.users.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(
            context.exception.detail,
            SubscriptionError.ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND
        )

    @patch('app.services.subscription_service.db')
    def test_create_subscription_fund_not_exist(self, mock_db):
        mock_db.users.find_one.return_value = {"id": "user123"}
        mock_db.funds.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(
            context.exception.detail,
            SubscriptionError.ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE
        )

    @patch('app.services.subscription_service.db')
    def test_cancel_subscription_success(self, mock_db):
        mock_db.subscriptions.update_one.return_value = None
        response = cancel_subscription("subscription123")
        self.assertEqual(
            response["detail"],
            SuccessMessage.SUCCESS_SUBSCRIPTION_CANCELLATION
        )

    @patch('app.services.subscription_service.db')
    def test_cancel_subscription_not_exist(self, mock_db):
        # Simulate that the subscription does not exist
        mock_db.subscriptions.find_one.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            cancel_subscription("non_existent_subscription_id")

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Subscription does not exist"
        mock_db.subscriptions.update_one.assert_not_called()

    @patch('app.services.subscription_service.db')
    def test_cancel_subscription_user_not_exist(self, mock_db):
        mock_db.subscriptions.find_one.return_value = {
            "user_id": "user123",
            "fund_id": "fund123"
        }  # Simulate that the subscription does not exist
        mock_db.users.find_one.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            cancel_subscription(
                SubscriptionError.ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND
            )

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == (
            SubscriptionError.ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND
        )
        mock_db.subscriptions.update_one.assert_not_called()

    @patch('app.services.subscription_service.db')
    def test_cancel_subscription_fund_not_exist(self, mock_db):
        # Simulate that the subscription does not exist
        mock_db.subscriptions.find_one.return_value = {
            "user_id": "user123",
            "fund_id": "fund123"
        }
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "investment_capital": 10000
        }
        mock_db.funds.find_one.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            cancel_subscription(
                SubscriptionError.ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE
            )

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == (
            SubscriptionError.ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE
        )
        mock_db.subscriptions.update_one.assert_not_called()

    @patch('app.services.subscription_service.db')
    def test_list_subscriptions_with_users(self, mock_db):
        mock_db.subscriptions.find.return_value = [
            {
                "_id": "sub123",
                "id": "sub123",
                "user_id": "user123",
                "fund_id": "fund123"
            }
        ]
        mock_db.users.find_one.return_value = {
            "_id": "user123",
            "name": "John Doe"
        }
        mock_db.funds.find_one.return_value = {
            "_id": "fund123",
            "name": "Fund A"
        }
        mock_db.transaction_history.find_one.return_value = {
            "_id": "trans123",
            "subscription_id": "sub123",
            "action": TransactionAction.CREATED,
            "notification_channel": "email",
            "timestamp": datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        }

        response = list_subscriptions_with_users()

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["subscription"]["user"]["name"], "John Doe")
        self.assertEqual(response[0]["subscription"]["fund"]["name"], "Fund A")

    @patch('app.services.subscription_service.db')
    def test_create_subscription_insufficient_investment_capital(self, mock_db):
        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "Fund A",
            "investment_capital": 500
        }
        mock_db.funds.find_one.return_value = {
            "id": "fund123",
            "name": "Fund A",
            "minimum_investment_amount": 1000
        }
        mock_db.subscriptions.find_one.return_value = None

        subscription = Subscription(
            user_id="user123",
            fund_id="fund123",
            status="active"
        )
        with self.assertRaises(HTTPException) as context:
            create_subscription(subscription)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            f"{SubscriptionError.ERROR_NO_AVAILABLE_BALANCE} Fund A"
        )

    @patch('app.services.subscription_service.db')
    def test_get_user_transactions_success(self, mock_db):
        user_id = "user123"
        mock_db.users.find_one.return_value = {
            "id": user_id,
            "_id": user_id,
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        mock_db.subscriptions.find.return_value = [
            {"id": "sub123", "user_id": user_id, "fund_id": "fund123"},
            {"id": "sub456", "user_id": user_id, "fund_id": "fund456"}
        ]
        mock_db.transaction_history.find.return_value = [
            {
                "_id": "trans123",
                "subscription_id": "sub123",
                "action": TransactionAction.CREATED,
                "timestamp": "2023-01-01T00:00:00Z"
            },
            {
                "_id": "trans456",
                "subscription_id": "sub456",
                "action": TransactionAction.CANCELLED,
                "timestamp": "2023-01-02T00:00:00Z"
            }
        ]
        mock_db.funds.find_one.side_effect = lambda query: {
            "id": query["id"],
            "_id": query["id"],
            "name": f"Fund {query['id'][-3:]}",
            "category": "Equity"
        }

        result = get_user_transactions(user_id)

        assert len(result) == 2

    @patch('app.services.subscription_service.db')
    def test_get_user_transactions_pymongo_error(self, mock_db):
        user_id = "user123"

        mock_db.users.find_one.return_value = {
            "id": "user123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "investment_capital": 10000
        }

        mock_db.subscriptions.find.side_effect = PyMongoError("Database error")

        with pytest.raises(HTTPException) as excinfo:
            get_user_transactions(user_id)

        assert excinfo.value.status_code == 500
        assert DataBaseError.ERROR_DB_CONNECTION in excinfo.value.detail

    @patch('app.services.subscription_service.db')
    def test_get_user_transactions_unexpected_error(self, mock_db):
        user_id = "user123"

        mock_db.users.find_one.return_value = None

        with pytest.raises(HTTPException) as excinfo:
            get_user_transactions(user_id)

        assert excinfo.value.status_code == 404
        assert SubscriptionError.ERROR_USER_DOEES_NOT_EXIST in excinfo.value.detail


if __name__ == '__main__':
    unittest.main()
