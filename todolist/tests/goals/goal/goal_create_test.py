import pytest
from django.utils import timezone

from tests.factories import UserFactory, USER_PASSWORD, GoalCategoryFactory


@pytest.mark.django_db
def test_create_goal(client, user: UserFactory):
    """
    Test successful goal creation
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category = GoalCategoryFactory.create(user=user)

    data = {
        'category': category.id,
        'title': 'Test goal',
        'description': '',
        'due_date': '2124-08-09',
        'status': 1,
        'priority': 1
    }

    expected_response = {
        'category': category.id,
        'created': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'updated': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'title': 'Test goal',
        'description': '',
        'due_date': '2124-08-09',
        'status': 1,
        'priority': 1
    }

    response = client.post('/goals/goal/create', data, format='json')

    response.data.pop('id')
    response.data['created'] = response.data['created'][:-11]
    response.data['updated'] = response.data['updated'][:-11]

    assert response.data == expected_response
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_goal_deleted_category(client, user: UserFactory):
    """
    Test goal creation with deleted category
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category = GoalCategoryFactory.create(user=user, is_deleted=True)

    data = {
        'category': category.id,
        'title': 'Test goal',
        'description': '',
        'due_date': '2124-08-09',
        'status': 1,
        'priority': 1
    }

    response = client.post('/goals/goal/create', data, format='json')

    assert response.data == {'category': ['Cannot use a deleted category']}
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_goal_not_category_owner(client, user: UserFactory):
    """
    Test goal creation with other user's category
    """
    client.login(username=user.username, password=USER_PASSWORD)

    other_user = UserFactory.create()
    category = GoalCategoryFactory.create(user=other_user)

    data = {
        'category': category.id,
        'title': 'Test goal',
        'description': '',
        'due_date': '2124-08-09',
        'status': 1,
        'priority': 1
    }

    response = client.post('/goals/goal/create', data, format='json')

    assert response.data == {'category': ['Not an owner of this category']}
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_goal_not_authenticated(client):
    """
    Test goal creation without authentication
    """
    data = {
        'category': 1,
        'title': 'Test goal',
        'description': '',
        'due_date': '2124-08-09',
        'status': 1,
        'priority': 1
    }

    response = client.post('/goals/goal/create', data, format='json')

    assert response.data == {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == 403
