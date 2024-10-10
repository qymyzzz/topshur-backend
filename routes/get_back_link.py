from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from db.database import users_collection
from routes.login import TokenData, get_current_user

router = APIRouter()


@router.get("/get_back_link")
async def get_back_link(token_data: TokenData = Depends(get_current_user)):
    try:
        username = token_data.username
        user = users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        back_link = user.get("back_link")
        return JSONResponse(content={"back_link": back_link}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
