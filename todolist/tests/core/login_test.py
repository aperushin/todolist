import pytest
from core.models import User
from django.urls import reverse
from rest_framework import status

from tests.factories import USER_PASSWORD


@pytest.mark.django_db
class TestLogin:
    url = reverse('core:login')

    def test_success(self, client, user: User, serialize_user):
        """User successfully logs in"""
        response = client.post(self.url, data={'username': user.username, 'password': USER_PASSWORD})

        assert response.data == serialize_user(user)
        assert response.status_code == status.HTTP_200_OK

    def test_incorrect_password(self, client, user: User):
        """User tries to log in with incorrect password and gets an authentication error"""
        response = client.post(self.url, data={'username': user.username, 'password': USER_PASSWORD + '1'})

        assert response.data == {'detail': 'Incorrect authentication credentials.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
