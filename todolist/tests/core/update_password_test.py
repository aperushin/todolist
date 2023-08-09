import pytest
from tests.factories import UserFactory, USER_PASSWORD


@pytest.mark.django_db
def test_update_password(client, user: UserFactory):
    """
    Test successful password update
    """
    client.login(username=user.username, password=USER_PASSWORD)

    new_password = USER_PASSWORD + '1'
    data = {
        'old_password': USER_PASSWORD,
        'new_password': new_password,
    }

    update_response = client.patch('/core/update_password', data, content_type='application/json')
    login_response = client.post(
        '/core/login',
        {'username': user.username, 'password': new_password},
        content_type='application/json',
    )

    assert update_response.status_code == 200
    assert login_response.status_code == 200


@pytest.mark.django_db
def test_update_password_incorrect_old(client, user: UserFactory):
    """
    Test password update with incorrect old password
    """
    client.login(username=user.username, password=USER_PASSWORD)

    new_password = USER_PASSWORD + '1'
    data = {
        'old_password': new_password,
        'new_password': new_password,
    }

    response = client.patch('/core/update_password', data, content_type='application/json')

    assert response.data == {'old_password': ['Old password is incorrect']}
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_password_unauthorized(client, user: UserFactory):
    """
    Test password update without authorization
    """
    new_password = USER_PASSWORD + '1'
    data = {
        'old_password': USER_PASSWORD,
        'new_password': new_password,
    }

    response = client.patch('/core/update_password', data, content_type='application/json')

    assert response.data == {'detail': 'Authentication credentials were not provided.'}
    assert response.status_code == 403
