import pytest

from tests.factories import UserFactory, USER_PASSWORD, GoalCategoryFactory
from goals.models import GoalCategory, Board, BoardParticipant


@pytest.mark.django_db
def test_destroy_category(client, user: UserFactory, board: Board, board_participant: BoardParticipant):
    """
    Test successfully getting a category
    """
    client.login(username=user.username, password=USER_PASSWORD)

    category: GoalCategory = GoalCategoryFactory.create(user=user, board=board)

    response = client.delete(f'/goals/goal_category/{category.id}')

    assert response.status_code == 204
