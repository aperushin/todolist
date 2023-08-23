import pytest
from rest_framework.test import APIClient
from typing import Callable
from unittest.mock import ANY

from core.models import User
from goals.models import BoardParticipant

pytest_plugins = 'tests.factories'


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client


@pytest.fixture
def created_updated_any() -> dict:
    return {'created': ANY, 'updated': ANY}


@pytest.fixture
def serialize_user() -> Callable:
    def _wrapper(user: User, **kwargs) -> dict:
        data = {
            'id': ANY,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        data |= kwargs
        return data
    return _wrapper


@pytest.fixture
def participant_data(created_updated_any) -> Callable:
    def _wrapper(board_participant: BoardParticipant = None, **kwargs) -> dict:
        data = {'role': BoardParticipant.Role.owner}
        if board_participant:
            data |= {
                'id': board_participant.id,
                'user': board_participant.user.username,
                'board': board_participant.board.id,
            }
        else:
            data |= {'id': ANY, 'user': ANY}
        data |= created_updated_any
        data |= kwargs
        return data
    return _wrapper


@pytest.fixture
def board_data(created_updated_any) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {
            'id': ANY,
            'title': 'Test board',
            'is_deleted': False,
        }
        data |= created_updated_any
        data |= kwargs
        return data
    return _wrapper


@pytest.fixture
def category_data(created_updated_any) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {
            'id': ANY,
            'title': 'Test category',
            'is_deleted': False,
        }
        data |= created_updated_any
        data |= kwargs
        return data
    return _wrapper


@pytest.fixture
def goal_data(created_updated_any) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {
            'id': ANY,
            'category': ANY,
            'title': 'Test goal',
            'description': 'Test description',
            'due_date': ANY,
            'status': 1,
            'priority': 1,
        }
        data |= created_updated_any
        data |= kwargs
        return data
    return _wrapper
