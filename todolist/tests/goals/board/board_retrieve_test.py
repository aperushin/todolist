import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board, BoardParticipant


@pytest.mark.django_db
def test_retrieve_board(auth_client, board_participant: BoardParticipant, board_data, participant_data):
    """Test successfully getting a board"""
    board: Board = board_participant.board

    response = auth_client.get(reverse('goals:board', args=[board.id]))

    assert response.data == board_data(
        id=board.id,
        title=board.title,
        participants=[participant_data(board_participant, board=board.id)],
    )
    assert response.status_code == status.HTTP_200_OK
