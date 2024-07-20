import io

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pymongo import MongoClient

from db.database import db
from routes.login import TokenData, get_current_user

router = APIRouter()

collection = db.audio_files


@router.get("/get-audio")
async def get_audio(transcript: str, token_data: TokenData = Depends(get_current_user)):
    try:
        username = token_data.username
        audio_file = collection.find_one(
            {"username": username, "transcript": transcript}
        )

        if not audio_file:
            raise HTTPException(status_code=404, detail="Audio file not found")

        audio_content = audio_file["audio_data"]
        content_type = audio_file["content_type"]

        return StreamingResponse(
            io.BytesIO(audio_content),
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={transcript}.wav"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
