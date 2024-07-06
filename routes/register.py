from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

from db.database import users_collection

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterUser(BaseModel):
    username: str
    password: str


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register", response_model=dict)
async def register_user(user: RegisterUser):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "hashed_password": hashed_password,
    }
    new_user = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return {"id": str(created_user["_id"]), "username": created_user["username"]}
