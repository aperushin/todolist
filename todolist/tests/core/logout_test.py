import pytest
from tests.factories import UserFactory, USER_PASSWORD


@pytest.mark.django_db
def test_logout(client, user: UserFactory):
    """
    Test successfully logging out
    """
    client.login(username=user.username, password=USER_PASSWORD)

    logout_response = client.delete('/core/profile')
    second_response = client.delete('/core/profile')

    assert logout_response.status_code == 204
    assert second_response.status_code == 403
