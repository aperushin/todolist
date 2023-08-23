import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_logout(auth_client):
    """User successfully logs out"""
    url = reverse('core:profile')

    logout_response = auth_client.delete(url)
    second_response = auth_client.delete(url)

    assert logout_response.status_code == status.HTTP_204_NO_CONTENT
    assert second_response.status_code == status.HTTP_403_FORBIDDEN
