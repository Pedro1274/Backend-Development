from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from backend.models import Task, TaskState


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TaskState)
    user_id = 1


def test_create_task(client, token):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_list_tasks_should_return_5_tasks(session, client, user, token):
    expected_tasks = 5
    session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/tasks/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_title_should_return_5_tasks(
    session, client, user, token
):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, title='Test task 1')
    )
    await session.commit()

    response = client.get(
        '/tasks/?title=Test task 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_description_should_return_5_tasks(
    session, client, user, token
):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, description='Test task 1')
    )
    await session.commit()

    response = client.get(
        '/tasks/?description=Test task 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_list_tasks_filter_state_should_return_5_tasks(
    session, client, user, token
):
    expected_tasks = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, state=TaskState.trash)
    )
    await session.commit()

    response = client.get(
        '/tasks/?state=trash', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['tasks']) == expected_tasks


@pytest.mark.asyncio
async def test_delete_task(session, client, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    await session.commit()

    response = client.delete(
        f'/tasks/{task.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Tarefa deletada com sucesso!'}


def test_delete_task_error(client, token):
    response = client.delete(
        '/tasks/7', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Tarefa não encontrada!'}


@pytest.mark.asyncio
async def test_patch_task(session, client, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    await session.commit()

    response = client.patch(
        f'/tasks/{task.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


def test_patch_task_error(client, token):
    response = client.patch(
        '/tasks/7',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Tarefa não encontrada!'}
