
import uuid
from datetime import datetime

from fastapi import HTTPException
from pymongo.errors import PyMongoError

from app.models.subscription import Subscription
from app.models.transaction_history import TransactionHistory
from app.utils.constants import (
    DataBaseError,
    FundStatus,
    SubscriptionError,
    SubscriptionNotificationChannel,
    SuccessMessage,
    TransactionAction
)
from app.utils.database import connect_db
from app.utils.formater.date_utils import DateUtils
from app.utils.notification.notification_factory import NotificationFactory

# load_dotenv()
db = connect_db()


def _send_subscription_notification(user: dict, fund: dict, method: str):
    """_summary_
    This function sends a notification to the user after a successful subscription
    Args:
        user (dict): _description_
        fund (dict): _description_
        method (str): _description_
    """

    subject = "Subscription Created Successfully"
    body = (
        f"Dear {user['name']},\n\n"
        f"Your subscription to {fund['name']} has been created successfully.\n\n"
        "Best regards,\n"
        "Your Company"
    )
    notification = NotificationFactory.get_notification(method)
    notification_channel_value = (
        user["email"]
        if method == SubscriptionNotificationChannel.EMAIL
        else user["phone_number"]
    )

    notification.send_notification(notification_channel_value, subject, body)


def create_subscription(subscription: Subscription):
    """_summary_
    This function creates a subscription for a user to a fund.
    Args:
        subscription (Subscription): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        e: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:

        # Check if the user exists
        user = db.users.find_one({"id": subscription.user_id})
        if not user:
            raise HTTPException(
                status_code=404,
                detail=SubscriptionError.ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND
            )

        # Check if the fund exists
        fund = db.funds.find_one({"id": subscription.fund_id})
        if not fund:
            raise HTTPException(
                status_code=404,
                detail=SubscriptionError.ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE
            )

        # Check if the user is already subscribed to the fund
        existing_subscription = db.subscriptions.find_one({
            "user_id": subscription.user_id,
            "fund_id": subscription.fund_id,
            "status": FundStatus.ACTIVE
        })

        if existing_subscription:
            raise HTTPException(
                status_code=400,
                detail=SubscriptionError.ERROR_USER_ALREADY_SUBSCRIBED_TO_FUND)

        user_investment_capital = user.get("investment_capital")
        fund_minimum_investment_amount = fund.get("minimum_investment_amount")

        if fund_minimum_investment_amount is None:
            raise HTTPException(
                status_code=400,
                detail=SubscriptionError.ERROR_NO_MINIMUM_AMOUNT_TO_INVEST
            )

        # Check if the user has enough investment capital to subscribe to the fund
        if user_investment_capital < fund_minimum_investment_amount:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"{str(SubscriptionError.ERROR_NO_AVAILABLE_BALANCE)} "
                    f"{fund['name']}"
                )
            )

        # Create the subscription
        subscription_id = str(uuid.uuid4())
        subscription_dict = subscription.dict()
        subscription_dict["id"] = subscription_id
        db.subscriptions.insert_one(subscription_dict)

        # Log the transaction
        log_transaction(
            subscription_id,
            TransactionAction.CREATED,
            subscription.subscription_notification_channel or
            SubscriptionNotificationChannel.EMAIL
        )

        """Subtract the fund's minimum investment amount
            from the user's investmen t capital"""
        new_investment_capital = (
            user_investment_capital
            - fund_minimum_investment_amount
        )

        db.users.update_one(
            {"id": subscription.user_id},
            {"$set": {"investment_capital": new_investment_capital}}
        )

        # Send notification
        _send_subscription_notification(
            user,
            fund,
            method=subscription.subscription_notification_channel or
            SubscriptionNotificationChannel.EMAIL
        )

        return {
            "detail": SuccessMessage.SUCCESS_SUBSCRIPTION,
            "subscription_id": subscription_id,
            "new_capital_value": new_investment_capital
        }

    except HTTPException as e:
        # Capturar y volver a lanzar la excepción HTTPException
        raise e
    except PyMongoError:
        raise HTTPException(status_code=500, detail=DataBaseError.ERROR_DB_CONNECTION)


def cancel_subscription(subscription_id: str):
    """_summary_
    This function cancels a subscription and refunds the user's investment capital.
    Args:
        subscription_id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        e: _description_

    Returns:
        _type_: _description_
    """
    try:
        # Check if the subscription exists
        subscription = db.subscriptions.find_one({"id": subscription_id})
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription does not exist")

        # Check if the user exists
        user = db.users.find_one({"id": subscription["user_id"]})
        if not user:
            raise HTTPException(
                status_code=404,
                detail=SubscriptionError.ERROR_USER_DOES_NOT_EXIST_TO_SUBSCRIBE_TO_FUND
            )

        # Check if the fund exists
        fund = db.funds.find_one({"id": subscription["fund_id"]})
        if not fund:
            raise HTTPException(
                status_code=404,
                detail=SubscriptionError.ERROR_FUND_DOES_NOT_EXIST_TO_SUBSCRIBE
            )

        user_investment_capital = user.get("investment_capital")
        fund_minimum_investment_amount = fund.get("minimum_investment_amount")
        new_investment_capital = (
            user_investment_capital + fund_minimum_investment_amount
        )

        db.users.update_one(
            {"id": user.get("id")},
            {"$set": {"investment_capital": new_investment_capital}}
        )

        db.subscriptions.update_one(
            {"id": subscription_id},
            {"$set": {"status": TransactionAction.CANCELLED}}
        )

        # Log the transaction
        log_transaction(
            subscription_id,
            TransactionAction.CANCELLED,
            str(subscription.get("subscription_notification_channel", "sin_canal"))
        )

        return {
            "detail": SuccessMessage.SUCCESS_SUBSCRIPTION_CANCELLATION,
            "new_capital_value": new_investment_capital
        }

    except HTTPException as e:
        raise e


def list_subscriptions_with_users():
    """_summary_
    This function returns a list of subscriptions with the user and fund information.
    Returns:
        _type_: _description_
    """
    subscriptions = db.subscriptions.find()
    result = []
    for subscription in subscriptions:
        user = db.users.find_one({"id": subscription["user_id"]})
        fund = db.funds.find_one({"id": subscription["fund_id"]})

        # Convert ObjectId to string
        subscription["_id"] = str(subscription["_id"])
        if user:
            user["_id"] = str(user["_id"])
            subscription["user"] = user
        if fund:
            fund["_id"] = str(fund["_id"])
            subscription["fund"] = fund

        # Find the latest transaction for the subscription
        transaction = db.transaction_history.find_one(
            {"subscription_id": subscription["id"]},
            sort=[("timestamp", -1)]
        )
        if transaction:
            subscription["transaction_timestamp"] = DateUtils.format_datetime(
                transaction["timestamp"]
            )

        # Remove user_id and fund_id from subscription
        subscription.pop("user_id", None)
        subscription.pop("fund_id", None)

        subscription_with_user_and_fund = {
            "subscription": subscription
        }

        result.append(subscription_with_user_and_fund)
    return result


def list_subscriptions_by_user(user_id: str):
    """
    This function returns a list of subscriptions for a user.
    Args: user_id (str): The user ID
    Returns: A list of subscriptions for the user
    """
    try:
        subscriptions = db.subscriptions.find({"user_id": user_id})
        result = []
        for subscription in subscriptions:
            user = db.users.find_one({"id": subscription["user_id"]})
            fund = db.funds.find_one({"id": subscription["fund_id"]})

            # Convertir ObjectId a string
            subscription["_id"] = str(subscription["_id"])
            if user:
                user["_id"] = str(user["_id"])
                subscription["user"] = user
            if fund:
                fund["_id"] = str(fund["_id"])
                subscription["fund"] = fund

            # Encontrar la última transacción para la suscripción
            transaction = db.transaction_history.find_one(
                {"subscription_id": subscription["id"]},
                sort=[("timestamp", -1)]
            )
            if transaction:
                subscription["transaction_timestamp"] = DateUtils.format_datetime(
                    transaction["timestamp"]
                )

            # Eliminar user_id y fund_id de la suscripción
            subscription.pop("user_id", None)
            subscription.pop("fund_id", None)

            result.append(subscription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_transactions(user_id: str):
    """_summary_
    This function returns a list of transactions for a user.
    Args:
        user_id (str): _description_

    Raises:
        HTTPException: _description_
        e: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        # Check if the user exists
        user = db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(
                status_code=404,
                detail=SubscriptionError.ERROR_USER_DOEES_NOT_EXIST
            )

        # Find all subscriptions for the user
        subscriptions = db.subscriptions.find({"user_id": user_id})
        subscription_ids = [subscription["id"] for subscription in subscriptions]

        # Find all transactions for the user's subscriptions
        transactions = db.transaction_history.find({
            "subscription_id": {"$in": subscription_ids}
        })

        result = []
        for transaction in transactions:
            transaction["_id"] = str(transaction["_id"])
            transaction["subscription_id"] = str(transaction["subscription_id"])

            # Get the user associated with the subscription
            subscription = db.subscriptions.find_one(
                {"id": transaction["subscription_id"]}
            )
            if subscription:
                user = db.users.find_one({"id": subscription["user_id"]})
                if user:
                    user["_id"] = str(user["_id"])
                    transaction["user"] = user

                fund = db.funds.find_one({"id": subscription["fund_id"]})
                if fund:
                    fund["_id"] = str(fund["_id"])
                    transaction["fund"] = fund

            result.append(transaction)

        return result

    except HTTPException as e:
        raise e
    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail=DataBaseError.ERROR_DB_CONNECTION
        )


def log_transaction(subscription_id: str, action: str, notification_channel: str):
    """_summary_
    This function logs a transaction in the transaction history collection.
    Args:
        subscription_id (str): _description_
        action (str): _description_
    """
    transaction = TransactionHistory(
        id=str(uuid.uuid4()),
        subscription_id=subscription_id,
        action=action,
        timestamp=datetime.utcnow(),
        notification_channel=notification_channel
    )
    db.transaction_history.insert_one(transaction.dict())
