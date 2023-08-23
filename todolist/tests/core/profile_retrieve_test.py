import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User


@pytest.mark.django_db
class TestRetrieveProfile:
    url = reverse('core:profile')

    def test_success(self, auth_client, user: User, serialize_user):
        """Test successfully getting profile data"""
        response = auth_client.get(self.url)

        assert response.data == serialize_user(user, id=user.id)
        assert response.status_code == status.HTTP_200_OK

    def test_no_auth(self, client):
        """Request without authentication returns an error"""
        response = client.get(self.url)

        assert response.data == {'detail': 'Authentication credentials were not provided.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
