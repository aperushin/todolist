import pytest
from tests.factories import UserFactory, USER_PASSWORD


@pytest.mark.django_db
def test_retrieve_profile(client, user: UserFactory):
    """
    Test successfully getting profile data
    """
    client.login(username=user.username, password=USER_PASSWORD)

    expected_response = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    response = client.get('/core/profile')
    response.data.pop('id')

    assert response.data == expected_response
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_profile_no_auth(client):
    """
    Test getting profile data without authentication
    """
    response = client.get('/core/profile')

    assert response.data == {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == 403
