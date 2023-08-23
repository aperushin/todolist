import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from goals.models import GoalCategory, Board, Goal, BoardParticipant


@pytest.mark.django_db
class TestDestroyCategory:
    @staticmethod
    def get_url(category_id: int) -> str:
        return reverse('goals:category', args=[category_id])

    def test_success(self, auth_client, user: User, board_factory, goal_category_factory, goal_factory):
        """Test successfully deleting a category"""
        board: Board = board_factory.create(with_owner=user)
        category: GoalCategory = goal_category_factory.create(user=user, board=board)
        goal: Goal = goal_factory.create(category=category)

        response = auth_client.delete(self.get_url(category.id))
        category.refresh_from_db()
        goal.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category.is_deleted
        assert goal.status == Goal.Status.archived

    def test_not_owner_or_writer(self, client, goal_category: GoalCategory, user_factory, board_participant_factory):
        """Reader participant cannot delete a category"""
        other_user = user_factory.create()
        board_participant_factory.create(board=goal_category.board, user=other_user, role=BoardParticipant.Role.reader)

        client.force_login(other_user)
        response = client.delete(self.get_url(goal_category.id))

        assert response.data == {'detail': 'You do not have permission to perform this action.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
