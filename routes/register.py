import os
from datetime import datetime, timedelta

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from db.database import users_collection

router = APIRouter()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterUser(BaseModel):
    username: str
    password: str
    disorder: str


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=dict)
async def register_user(user: RegisterUser):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "hashed_password": hashed_password,
        "disorder": user.disorder,
    }
    new_user = users_collection.insert_one(user_data)
    created_user = users_collection.find_one({"_id": new_user.inserted_id})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": created_user["username"]}, expires_delta=access_token_expires
    )

    return {
        "id": str(created_user["_id"]),
        "username": created_user["username"],
        "disorder": created_user["disorder"],
        "access_token": access_token,
        "token_type": "bearer",
    }
