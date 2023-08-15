import pytest

from core.models import User
from tests.factories import USER_PASSWORD


@pytest.mark.django_db
def test_create_board(client, user: User, helpers, formatted_now):
    """
    Test successful board creation
    """
    client.login(username=user.username, password=USER_PASSWORD)

    data = {
        'title': 'Test board',
    }

    expected_response = {
        'title': 'Test board',
        'created': formatted_now,
        'updated': formatted_now,
        'is_deleted': False,
    }

    response = client.post('/goals/board/create', data, format='json')

    response.data.pop('id')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_board_not_authenticated(client):
    """
    Test board creation without authentication
    """
    data = {
        'title': 'Test category',
    }

    response = client.post('/goals/board/create', data, format='json')

    assert response.data == {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == 403
