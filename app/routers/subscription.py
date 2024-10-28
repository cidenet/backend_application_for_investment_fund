# subscription.py
from fastapi import APIRouter
from app.models.subscription import Subscription
from app.services.subscription_service import (
    create_subscription,
    cancel_subscription,
    list_subscriptions_by_user,
    list_subscriptions_with_users,
    get_user_transactions
)

router = APIRouter()


@router.post("/subscriptions/")
def create_subscription_endpoint(subscription: Subscription):
    return create_subscription(subscription)


@router.post("/subscriptions/cancel/{subscription_id}")
def cancel_subscription_endpoint(subscription_id: str):
    return cancel_subscription(subscription_id)


@router.get("/subscriptions/")
def list_subscriptions_with_users_endpoint():
    return list_subscriptions_with_users()


@router.get("/subscriptions/{user_id}/transactions")
def get_user_transactions_endpoint(user_id: str):
    return get_user_transactions(user_id)


@router.get("/subscriptions/user/{user_id}")
def get_subscriptions_by_user(user_id: str):
    subscriptions = list_subscriptions_by_user(user_id)
    # if not subscriptions:
    #     raise HTTPException(
    # status_code=404, detail="No subscriptions found for this user")
    return subscriptions
