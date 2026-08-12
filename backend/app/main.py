from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app import auth, chats
from fastapi.concurrency import run_in_threadpool

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # init_db()
    await run_in_threadpool(init_db)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

app.include_router(auth.router)
app.include_router(chats.router)

@app.get('/health')
def health() -> dict[str, str]:
    return {"status": "ok"}

