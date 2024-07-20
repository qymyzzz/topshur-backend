from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from db.database import db
from routes.login import TokenData, get_current_user

router = APIRouter()

collection = db.audio_files


@router.get("/get-audios")
async def get_audios(token_data: TokenData = Depends(get_current_user)):
    try:
        username = token_data.username
        audio_files = collection.find({"username": username})
        transcripts = [file["transcript"] for file in audio_files]
        return JSONResponse(content={"transcripts": transcripts}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
