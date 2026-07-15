from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from backend.models import Task, User
from backend.schemas import FilterTask, TaskList, TaskPublic, TaskSchema
from backend.security import get_current_user

router = APIRouter(tags=['tasks'], prefix='/tasks')

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
async def create_task(task: TaskSchema, session: Session, user: CurrentUser):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.get('/', status_code=HTTPStatus.OK, response_model=TaskList)
async def get_task(
    user: CurrentUser,
    session: Session,
    task_filter: Annotated[FilterTask, Query()],
):
    query = select(Task).where(Task.user_id == user.id)

    if task_filter.title:
        query = query.filter(Task.title.contains(task_filter.title))

    if task_filter.description:
        query = query.filter(
            Task.description.contains(task_filter.description)
        )

    if task_filter.state:
        query = query.filter(Task.state.contains(task_filter.state))

    tasks = await session.scalars(
        query.limit(task_filter.limit).offset(task_filter.offset)
    )

    return {'tasks': tasks.all()}
