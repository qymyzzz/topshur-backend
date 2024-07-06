import mimetypes

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from db.database import db
from routes.login import TokenData, get_current_user

router = APIRouter()

collection = db.audio_files

ALLOWED_AUDIO_TYPES = [
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/ogg",
    "application/octet-stream",
]
ALLOWED_EXTENSIONS = [".mp3", ".wav", ".ogg"]


@router.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...), token_data: TokenData = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed types are MP3, WAV, and OGG.",
        )

    file_id = str(ObjectId())
    audio_content = await file.read()

    audio_document = {
        "_id": file_id,
        "username": token_data.username,
        "content_type": file.content_type,
        "audio_data": audio_content,
    }

    await collection.insert_one(audio_document)

    return JSONResponse(content={"file_id": file_id}, status_code=201)
