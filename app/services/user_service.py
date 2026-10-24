from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.repositories.user_repo import IUserRepository
from app.schemas.user_model import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, repository: IUserRepository):
        self._repo = repository


    async def create_user(self, data: UserCreate) -> UserResponse:
        existing_user = await self._repo.get_by_email(data.email)
        if existing_user:
            raise EmailAlreadyExistsError(data.email)

        record = await self._repo.create(data)
        return UserResponse(**dict(record))

    async def get_all(self, skip: int, limit: int) -> list[UserResponse]:
        records = await self._repo.get_all(skip, limit)
        return [UserResponse(**dict(record)) for record in records]

    async def get_by_id(self, user_id: int) -> UserResponse:
        record = await self._repo.get_by_id(user_id)
        if record is None:
            raise UserNotFoundError(user_id)
        return UserResponse(**dict(record))

    async def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        await self.get_by_id(user_id)
        await self._ensure_email_avaialable(data.email, exclude_user_id=user_id)

        record = await self._repo.update(user_id, data)
        return UserResponse(**dict(record))

    async def delete_user(self, user_id: int) -> None:
        was_deleted = await self._repo.delete(user_id)
        if not was_deleted:
            raise UserNotFoundError(user_id)


    async def _ensure_email_avaialable(
            self,email: str, exclude_user_id: int | None = None
    ) -> None:
        existing_user = await self._repo.get_by_email(email)
        if existing_user and existing_user["id"] != exclude_user_id:
            raise EmailAlreadyExistsError(email)