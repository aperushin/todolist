import pytest
from tests.factories import UserFactory, USER_PASSWORD, GoalCategoryFactory


@pytest.mark.django_db
def test_list_category(client, user: UserFactory):
    """
    Test successfully getting paginated category list
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category_count = 5

    GoalCategoryFactory.create_batch(category_count, user=user)
    GoalCategoryFactory.create_batch(1, user=user, is_deleted=True)

    expected_response = {
        'count': category_count,
        'next': None,
        'previous': None,
    }

    response = client.get('/goals/goal_category/list?limit=10')
    results = response.data.pop('results')

    assert response.data == expected_response
    assert len(results) == category_count
    assert response.status_code == 200
