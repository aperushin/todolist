import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board, BoardParticipant


@pytest.mark.django_db
class TestCreateCategory:
    url = reverse('goals:create-category')

    def test_success(self, auth_client, board_participant: BoardParticipant, category_data):
        """Test successful category creation"""
        board: Board = board_participant.board

        response = auth_client.post(self.url, data={'title': 'Test category', 'board': board.id})

        assert response.data == category_data(board=board.id)
        assert response.status_code == status.HTTP_201_CREATED

    def test_not_authenticated(self, client):
        """Request without authentication returns an error"""
        response = client.post(self.url, data={'title': 'Test category'})

        assert response.data == {'detail': 'Authentication credentials were not provided.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
