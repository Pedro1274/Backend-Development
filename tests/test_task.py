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
    assert response.status_code == HTTPStatus.OK
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


# Continuar as rotas