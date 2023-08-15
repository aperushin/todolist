import pytest

from tests.factories import USER_PASSWORD, UserFactory, BoardParticipantFactory
from core.models import User
from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_update_board(client, user: User, board: Board, board_participant: BoardParticipant, formatted_now, helpers):
    """
    Test successful board update
    """
    client.login(username=user.username, password=USER_PASSWORD)
    other_user = UserFactory.create(username='test participant')

    data = {
        'title': 'Test category',
        'participants': [
            {
                'role': 2,
                'user': other_user.username,
            }
        ]
    }

    expected_response = {
        'id': board.id,
        'title': 'Test category',
        'participants': [
            {
                'id': board_participant.id,
                'user': board_participant.user.username,
                'board': board.id,
                'role': BoardParticipant.Role.owner,
                'created': formatted_now,
                'updated': formatted_now,
            },
            {
                'id': board_participant.id + 1,
                'user': other_user.username,
                'board': board.id,
                'role': 2,
                'created': formatted_now,
                'updated': formatted_now,
            },
        ],
        'created': formatted_now,
        'updated': formatted_now,
        'is_deleted': board.is_deleted,
    }

    response = client.put(f'/goals/board/{board.id}', data, content_type='application/json')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_board_remove_participants(
        client, user: User, board: Board, board_participant: BoardParticipant, formatted_now, helpers
):
    """
    Test successful board update with participant removal
    """
    client.login(username=user.username, password=USER_PASSWORD)
    other_user = UserFactory.create(username='test participant')
    BoardParticipantFactory.create(board=board, user=other_user, role=BoardParticipant.Role.writer)

    data = {
        'title': 'Test category',
        'participants': []
    }

    expected_response = {
        'id': board.id,
        'title': 'Test category',
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

    response = client.put(f'/goals/board/{board.id}', data, content_type='application/json')
    helpers.trim_dates(response.data)

    assert response.data == expected_response
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_board_set_owner(client, user: User, board: Board, board_participant: BoardParticipant):
    """
    Test board update with an attempt to add a second owner
    """
    client.login(username=user.username, password=USER_PASSWORD)
    other_user = UserFactory.create(username='test participant')

    data = {
        'title': 'Test category',
        'participants': [
            {
                'role': 1,
                'user': other_user.username,
            }
        ]
    }

    response = client.put(f'/goals/board/{board.id}', data, content_type='application/json')

    assert response.data == {'participants': [{'role': ['"1" is not a valid choice.']}]}
    assert response.status_code == 400
