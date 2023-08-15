import pytest

from tests.factories import USER_PASSWORD
from core.models import User
from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_create_category(client, user: User, board: Board, formatted_now, helpers, board_participant: BoardParticipant):
    """
    Test successful category creation
    """
    client.login(username=user.username, password=USER_PASSWORD)

    data = {
        'title': 'Test category',
        'board': board.id,
    }

    expected_response = {
        'title': 'Test category',
        'board': board.id,
        'created': formatted_now,
        'updated': formatted_now,
        'is_deleted': False,
    }

    response = client.post('/goals/goal_category/create', data, format='json')

    response.data.pop('id')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_category_not_authenticated(client):
    """
    Test category creation without authentication
    """
    data = {
        'title': 'Test category',
    }

    response = client.post('/goals/goal_category/create', data, format='json')

    assert response.data == {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == 403
