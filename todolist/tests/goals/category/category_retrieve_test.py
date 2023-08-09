import pytest
from django.utils import timezone

from tests.factories import UserFactory, USER_PASSWORD, GoalCategoryFactory
from core.serializers import ProfileSerializer
from goals.models import GoalCategory


@pytest.mark.django_db
def test_retrieve_category(client, user: UserFactory):
    """
    Test successfully getting a category
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category: GoalCategory = GoalCategoryFactory.create(user=user)

    expected_response = {
        'id': category.id,
        'title': category.title,
        'user': ProfileSerializer(user).data,
        'created': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'updated': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        'is_deleted': category.is_deleted,
    }

    response = client.get(f'/goals/goal_category/{category.id}')
    response.data['created'] = response.data['created'][:-11]
    response.data['updated'] = response.data['updated'][:-11]

    assert response.data == expected_response
    assert response.status_code == 200
