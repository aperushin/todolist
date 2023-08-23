import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from tests.factories import USER_PASSWORD


@pytest.mark.django_db
class TestRetrieveProfile:
    url = reverse('core:update-password')
    login_url = reverse('core:login')

    def test_success(self, auth_client, client, user: User):
        """Test successful password update"""
        new_password = USER_PASSWORD + '1'
        data = {'old_password': USER_PASSWORD, 'new_password': new_password}

        update_response = auth_client.patch(self.url, data)
        login_response = client.post(self.login_url, data={'username': user.username, 'password': new_password})

        assert update_response.status_code == status.HTTP_200_OK
        assert login_response.status_code == status.HTTP_200_OK

    def test_incorrect_old_password(self, auth_client, user: User):
        """Request with incorrect old password returns an error"""
        new_password = USER_PASSWORD + '1'
        data = {'old_password': new_password, 'new_password': new_password}

        response = auth_client.patch(self.url, data)

        assert response.data == {'old_password': ['Old password is incorrect']}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_password_unauthorized(self, client, user: User):
        """Request without authentication returns an error"""
        new_password = USER_PASSWORD + '1'
        data = {'old_password': USER_PASSWORD, 'new_password': new_password}

        response = client.patch('/core/update_password', data)

        assert response.data == {'detail': 'Authentication credentials were not provided.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
