from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.add_disorder import router as disorder_router
from routes.login import router as login_router
from routes.register import router as register_router
from routes.upload_audio import router as audio_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://nneurons.vercel.app/",
    "http://topshur.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(audio_router)
app.include_router(login_router, tags=["login"])
app.include_router(disorder_router)
app.include_router(register_router, tags=["register"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

# python -m uvicorn main:app --reload
