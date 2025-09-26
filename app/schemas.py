from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class UserDB(UserSchema):
    id: int


class UserPublic(UserDB):
    password: Optional[SecretStr] = Field(None, exclude=True)


class UserList(BaseModel):
    users: list[UserPublic]
