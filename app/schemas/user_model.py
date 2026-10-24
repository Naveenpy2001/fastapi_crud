from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    gender: Gender
    phone_number: str  = Field(pattern=r'^\+?[0-9]{10,14}$')
    is_active: bool = True

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    gender: Gender
    phone_number: str
    is_active: bool


class UserUpdate(UserCreate):
    pass

class UserPatch(BaseModel):

    full_name: str | None = Field(default=None)
    email: EmailStr | None = None
    gender:  Gender | None = None
    phone_number: str | None = None
    is_active: bool | None = None