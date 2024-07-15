import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.database import users_collection

router = APIRouter()
load_dotenv()


class AddDisorder(BaseModel):
    username: str
    disorder: str


@router.post("/add_disorder", response_model=dict)
async def add_disorder(add_disorder_data: AddDisorder):
    existing_user = users_collection.find_one({"username": add_disorder_data.username})
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    users_collection.update_one(
        {"username": add_disorder_data.username},
        {"$set": {"disorder": add_disorder_data.disorder}},
    )
    updated_user_data = users_collection.find_one(
        {"username": add_disorder_data.username}
    )

    return {
        "id": str(updated_user_data["_id"]),
        "username": updated_user_data["username"],
        "disorder": updated_user_data["disorder"],
    }
