import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCreateBoard:
    url = reverse('goals:create-board')

    def test_create_board(self, auth_client, board_data):
        """Test successful board creation"""
        response = auth_client.post(self.url, data={'title': 'Test board'})

        assert response.data == board_data()
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_board_not_authenticated(self, client):
        """Request without authentication returns an error"""
        response = client.post(self.url, data={'title': 'Test category'})

        assert response.data == {'detail': 'Authentication credentials were not provided.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
