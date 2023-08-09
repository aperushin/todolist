import pytest


@pytest.mark.django_db
def test_create_user(client):
    """
    Test successful user creation
    """
    data = {
      'username': 'test_user',
      'first_name': 'Test',
      'last_name': 'Test',
      'email': 'user@example.com',
      'password': '123afafa',
      'password_repeat': '123afafa'
    }

    expected_response = {
      'username': 'test_user',
      'first_name': 'Test',
      'last_name': 'Test',
      'email': 'user@example.com'
    }

    response = client.post('/core/signup', data, format='json')
    response.data.pop('id')

    assert response.data == expected_response
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_user_password_mismatch(client):
    """
    Test user creation with incorrectly repeated password
    """
    data = {
      'username': 'test_user_1',
      'first_name': 'Test',
      'last_name': 'Test',
      'email': 'user@example.com',
      'password': '123afafa',
      'password_repeat': '123afafaf'
    }

    response = client.post('/core/signup', data, format='json')

    assert response.data == {'password_repeat': ['Passwords do not match']}
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_user_password_too_simple(client):
    """
    Test user creation with a weak password
    """
    data = {
      'username': 'test_user_2',
      'first_name': 'Test',
      'last_name': 'Test',
      'email': 'user@example.com',
      'password': '123',
      'password_repeat': '123'
    }

    expected_response = {
        'password': [
            'This password is too short. It must contain at least 8 characters.',
            'This password is too common.',
            'This password is entirely numeric.',
        ],
        'password_repeat': [
            'This password is too short. It must contain at least 8 characters.',
            'This password is too common.',
            'This password is entirely numeric.',
        ]
    }

    response = client.post('/core/signup', data, format='json')

    assert response.data == expected_response
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_user_already_exists(client):
    """
    Test user creation with existing username
    """
    data = {
      'username': 'test_user_3',
      'first_name': 'Test',
      'last_name': 'Test',
      'email': 'user@example.com',
      'password': '123afafa',
      'password_repeat': '123afafa'
    }

    expected_response = {'username': ['A user with that username already exists.']}

    # Posting same data twice
    _ = client.post('/core/signup', data, format='json')
    response = client.post('/core/signup', data, format='json')

    assert response.data == expected_response
    assert response.status_code == 400
