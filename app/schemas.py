from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserPublic(UserDB):
    password: Optional[str] = Field(None, exclude=True)


class UserList(BaseModel):
    users: list[UserPublic]
