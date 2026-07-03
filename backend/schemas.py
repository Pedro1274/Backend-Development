from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr


class UserSchema(UserPublic):
    id: int
    password: str


class UserDB(UserSchema):
    id: int
