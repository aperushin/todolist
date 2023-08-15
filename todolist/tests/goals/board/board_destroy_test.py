import pytest

from core.models import User
from goals.models import Board, GoalCategory, Goal
from tests.factories import USER_PASSWORD, GoalFactory, GoalCategoryFactory, BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_destroy_board(client, user: User):
    """
    Test successful board deletion
    """
    client.login(username=user.username, password=USER_PASSWORD)

    board = BoardFactory.create()
    BoardParticipantFactory.create(user=user, board=board)

    category = GoalCategoryFactory.create(user=user, board=board)
    goal = GoalFactory.create(user=user, category=category)

    response = client.delete(f'/goals/board/{board.id}')

    assert Board.objects.get(id=board.id).is_deleted
    assert GoalCategory.objects.get(id=category.id).is_deleted
    assert Goal.objects.get(id=goal.id).status == Goal.Status.archived
    assert response.status_code == 204
