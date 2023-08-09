import pytest
from django.utils import timezone

from tests.factories import UserFactory, USER_PASSWORD


@pytest.mark.django_db
def test_create_category(client, user: UserFactory):
    """
    Test successful category creation
    """
    client.login(username=user.username, password=USER_PASSWORD)

    data = {
        'title': 'Test category',
    }

    expected_response = {
        'title': 'Test category',
        'created': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'updated': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'is_deleted': False,
    }

    response = client.post('/goals/goal_category/create', data, format='json')

    response.data.pop('id')
    response.data['created'] = response.data['created'][:-11]
    response.data['updated'] = response.data['updated'][:-11]

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
