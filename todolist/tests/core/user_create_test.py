import pytest
from django.urls import reverse
from rest_framework import status
from typing import Callable

from core.models import User


@pytest.fixture
def user_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {
            'username': faker.user_name(),
            'first_name': faker.name(),
            'last_name': faker.name(),
            'email': faker.email(),
        }
        data |= kwargs
        return data
    return _wrapper


@pytest.mark.django_db
class TestCreateUser:
    url: str = reverse('core:signup')
    valid_password: str = '123afafa'

    def test_success(self, client, user_create_data, serialize_user):
        """Test successful user creation"""
        data: dict = user_create_data(password=self.valid_password, password_repeat=self.valid_password)

        response = client.post(self.url, data=data)

        assert response.data == serialize_user(User.objects.last())
        assert response.status_code == status.HTTP_201_CREATED

    def test_password_mismatch(self, client, user_create_data):
        """Request with incorrectly repeated password returns an error"""
        data = user_create_data(password=self.valid_password, password_repeat=(self.valid_password + '1'))

        response = client.post(self.url, data)

        assert response.data == {'password_repeat': ['Passwords do not match']}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_simple(self, client, user_create_data):
        """Request with a weak password returns an error"""
        weak_password = '123'
        data = user_create_data(password=weak_password, password_repeat=weak_password)
        expected_errors = [
            'This password is too short. It must contain at least 8 characters.',
            'This password is too common.',
            'This password is entirely numeric.',
        ]

        response = client.post(self.url, data)

        assert response.data == {'password': expected_errors, 'password_repeat': expected_errors}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_already_exists(self, client, user_create_data):
        """Request with an existing username returns an error"""
        data = user_create_data(password=self.valid_password, password_repeat=self.valid_password)

        # Posting same data twice
        client.post(self.url, data)
        response = client.post(self.url, data)

        assert response.data == {'username': ['A user with that username already exists.']}
        assert response.status_code == status.HTTP_400_BAD_REQUEST
