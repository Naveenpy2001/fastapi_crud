import asyncpg
from asyncpg import Pool
from app.core.config import settings


class Database:
    def __init__(self) -> None:
        self._pool : Pool | None = None


    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=1,
            max_size=10,
        )
        print("Database pool created..")


    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()

            print("Database pool closed..")

    def get_pool(self):
        if self._pool is None:
            raise RuntimeError("Database is not connected")
        return self._pool


database = Database()