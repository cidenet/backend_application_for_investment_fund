import uuid
from app.utils.database import connect_db
from app.models.user import User
from pymongo.errors import PyMongoError
from fastapi import HTTPException

db = connect_db()


def create_user(user: User):
    try:
        user_id = str(uuid.uuid4())
        user_dict = user.dict()

        if user_dict["investment_capital"] is None:
            user_dict["investment_capital"] = 500000.0

        user_dict["id"] = user_id  # Set the generated UUID as the id field
        db.users.insert_one(user_dict)
        return {"message": "User created successfully", "user_id": user_id}
    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user: " + str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred: " + str(e)
        )


def get_all_users():
    try:
        # Exclude the MongoDB internal _id field
        users = list(db.users.find({}, {"_id": 0}))

        for user in users:
            user["id"] = str(user["id"])  # Convert the ObjectId to a string
        return users
    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching users: " + str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred: " + str(e)
        )
