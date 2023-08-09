import pytest
from tests.factories import UserFactory, USER_PASSWORD


@pytest.mark.django_db
def test_login(client, user: UserFactory):
    """
    Test successful login
    """
    data = {
        'username': user.username,
        'password': USER_PASSWORD,
    }

    expected_response = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    response = client.post('/core/login', data, format='json')
    response.data.pop('id')

    assert response.data == expected_response
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_incorrect_password(client, user: UserFactory):
    """
    Test login with incorrect password
    """
    data = {
        'username': user.username,
        'password': USER_PASSWORD + '1',
    }

    expected_response = {'detail': 'Incorrect authentication credentials.'}

    response = client.post('/core/login', data, format='json')

    assert response.data == expected_response
    assert response.status_code == 403
