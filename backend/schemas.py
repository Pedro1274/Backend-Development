from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.models import TaskState


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)


class FilterTask(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=20)
    description: str | None = None
    state: TaskState | None = None


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState = Field(default=TaskState.draft)


class TaskPublic(TaskSchema):
    id: int


class TaskList(BaseModel):
    tasks: list[TaskPublic]
