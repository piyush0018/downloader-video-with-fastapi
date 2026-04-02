from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import video, audio
from utils.file_utils import ensure_directories

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(video.router)
app.include_router(audio.router)