from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import database
from app.routers.user_router import router as user_router


origins = [
    "http://localhost:5173"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title="User API",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

@app.get("/")
async def root():
    return {"message" : "User API is running..."}

@app.get("/health/db")
async def health_db():
    pool = database.get_pool()
    async with pool.acquire() as connection:
        result = await connection.fetchval("SELECT 1")
    return {"database" : "connected","test_query_result" : result}