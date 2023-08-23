import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from goals.models import BoardParticipant


@pytest.mark.django_db
def test_retrieve_category(
        auth_client, user: User, serialize_user, board_participant: BoardParticipant, goal_category, category_data
):
    """Test successfully getting a category """
    board = board_participant.board

    response = auth_client.get(reverse('goals:category', args=[goal_category.id]))

    assert response.data == category_data(id=goal_category.id, board=board.id, user=serialize_user(user))
    assert response.status_code == status.HTTP_200_OK
