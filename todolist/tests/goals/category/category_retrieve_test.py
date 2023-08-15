import pytest

from tests.factories import USER_PASSWORD, GoalCategoryFactory
from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Board, BoardParticipant


@pytest.mark.django_db
def test_retrieve_category(
        client, user: User, board: Board, helpers, formatted_now, board_participant: BoardParticipant
):
    """
    Test successfully getting a category
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category: GoalCategory = GoalCategoryFactory.create(user=user, board=board)

    expected_response = {
        'id': category.id,
        'title': category.title,
        'board': board.id,
        'user': ProfileSerializer(user).data,
        'created': formatted_now,
        'updated': formatted_now,
        'is_deleted': category.is_deleted,
    }

    response = client.get(f'/goals/goal_category/{category.id}')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 200
