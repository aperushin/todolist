import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from goals.models import Board, GoalCategory, Goal


@pytest.mark.django_db
def test_destroy_board(auth_client, user: User, board_factory, goal_category_factory, goal_factory):
    """Test successful board deletion"""
    board = board_factory.create(with_owner=user)
    category = goal_category_factory.create(user=user, board=board)
    goal = goal_factory.create(user=user, category=category)

    response = auth_client.delete(reverse('goals:board', args=[board.id]))

    assert Board.objects.get(id=board.id).is_deleted
    assert GoalCategory.objects.get(id=category.id).is_deleted
    assert Goal.objects.get(id=goal.id).status == Goal.Status.archived
    assert response.status_code == status.HTTP_204_NO_CONTENT
