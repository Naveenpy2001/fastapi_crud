from fastapi import Depends

from app.db.database import database
from app.repositories.user_repo import IUserRepository, UserRepositiry
from app.services.user_service import UserService


def get_user_repository() -> IUserRepository:
    return UserRepositiry(database.get_pool())


def get_user_service(
        repository: IUserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)