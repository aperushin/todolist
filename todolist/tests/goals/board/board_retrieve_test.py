import pytest

from tests.factories import USER_PASSWORD
from core.models import User
from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_retrieve_board(client, user: User, board: Board, board_participant: BoardParticipant, helpers, formatted_now):
    """
    Test successfully getting a board
    """
    client.login(username=user.username, password=USER_PASSWORD)

    expected_response = {
        'id': board.id,
        'title': board.title,
        'participants': [
            {
                'id': board_participant.id,
                'user': board_participant.user.username,
                'board': board.id,
                'role': BoardParticipant.Role.owner,
                'created': formatted_now,
                'updated': formatted_now,
            },
        ],
        'created': formatted_now,
        'updated': formatted_now,
        'is_deleted': board.is_deleted,
    }

    response = client.get(f'/goals/board/{board.id}')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 200
