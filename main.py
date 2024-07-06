from fastapi import FastAPI

from routes.login import router as login_router
from routes.register import router as register_router
from routes.upload_audio import router as audio_router

app = FastAPI()

app.include_router(audio_router)
app.include_router(login_router, tags=["login"])
app.include_router(register_router, tags=["register"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

# python -m uvicorn main:app --reload
