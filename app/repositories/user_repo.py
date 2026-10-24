from abc import ABC,abstractmethod
from typing import Any
from asyncpg import Pool, Record

from app.schemas.user_model import UserCreate,UserUpdate

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, data: UserCreate) -> Record: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Record | None: ...

    @abstractmethod
    async def get_all(self, skip: int, limit: int) -> list[Record]: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Record | None: ...

    @abstractmethod
    async def update(self, user_id:int, data: UserCreate) -> Record | None: ...

    @abstractmethod
    async def delete(self, user_id: int) -> bool: ...

    # @abstractmethod
    # async def patch(self, user_id: int, fields: dict[str, Any]) -> Record | None: ...


class UserRepositiry(IUserRepository):
    def __init__(self, pool: Pool) -> None:
        self._pool = pool


    async def create(self, data: UserCreate) -> Record:
        query = """
            INSERT INTO users (full_name, email, gender,phone_number,is_active)
            VALUES ($1,$2,$3,$4,$5)
            RETURNING id, full_name,email,gender, phone_number, is_active
        """
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                data.full_name,
                data.email,
                data.gender,
                data.phone_number,
                data.is_active
            )

    async def get_by_email(self, email: str) -> Record | None:
        query = "SELECT id from users WHERE email = $1"
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query,email)


    async def get_all(self, skip: int, limit: int) -> list[Record]:
        query = """
                SELECT * FROM users
                ORDER BY id
                OFFSET $1
                LIMIT $2
            """ 

        async with self._pool.acquire() as conn:
            return await conn.fetch(query, skip, limit)

    async def get_by_id(self, user_id: int) -> Record | None:
        query = """
                SELECT * FROM users
                WHERE id = $1
            """
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, user_id)


    async def update(self, user_id: int, data: UserUpdate):
        query = """
                UPDATE users 
                SET full_name = $1,
                    email = $2,
                    gender = $3,
                    phone_number = $4,
                    is_active = $5
                WHERE id = $6
                RETURNING id, full_name, email,gender, phone_number, is_active
            """
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                data.full_name,
                data.email,
                data.gender, #todo:  need to add .value for gender | check without value 1st...
                data.phone_number,
                data.is_active,
                user_id
            )

    async def delete(self, user_id : int) -> bool:
        query = """
            DELETE FROM users WHERE id = $1 RETURNING id
        """
        async with self._pool.acquire() as conn:
            deleted_id = await conn.fetchval(query, user_id)
        return deleted_id is not None

        