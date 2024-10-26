# user.py
from fastapi import APIRouter
from app.models.user import User
from app.services.user_service import create_user, get_all_users

router = APIRouter()


@router.post("/users/")
def create_user_endpoint(user: User):
    return create_user(user)


@router.get("/users/")
def get_all_users_endpoint():
    return get_all_users()
