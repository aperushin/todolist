import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board, BoardParticipant


@pytest.mark.django_db
class TestUpdateBoard:
    @staticmethod
    def get_url(board_id: int) -> str:
        return reverse('goals:board', args=[board_id])

    @staticmethod
    def get_update_data(**kwargs) -> dict:
        data = {'title': 'Test board', 'participants': []}
        data |= kwargs
        return data

    def test_update_board(
            self,
            auth_client,
            user_factory,
            board: Board,
            board_participant: BoardParticipant,
            board_data,
            participant_data,
    ):
        """Successfully add a participant to a board"""
        other_user = user_factory.create(username='test participant')
        new_participant_data = {'role': BoardParticipant.Role.writer, 'user': other_user.username}
        result_participants = [
            participant_data(board_participant=board_participant),
            participant_data(board=board.id, **new_participant_data),
        ]

        response = auth_client.put(
            self.get_url(board.id),
            self.get_update_data(participants=[new_participant_data]),
        )

        assert response.data == board_data(id=board.id, participants=result_participants)
        assert response.status_code == status.HTTP_200_OK

    def test_update_board_remove_participants(
            self,
            auth_client,
            user_factory,
            board_participant_factory,
            board: Board,
            board_participant: BoardParticipant,
            participant_data,
            board_data,
    ):
        """Update with an empty participant list removes all participants except the owner"""
        other_user = user_factory.create(username='test participant')
        board_participant_factory.create(board=board, user=other_user, role=BoardParticipant.Role.writer)
        expected_response = board_data(
            id=board.id,
            participants=[participant_data(board_participant=board_participant)],
        )

        response = auth_client.put(self.get_url(board.id), self.get_update_data(participants=[]))

        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK

    def test_update_board_set_owner(self, auth_client, user_factory, board_participant: BoardParticipant):
        """An attempt to add a second owner participant returns an error"""
        board: Board = board_participant.board
        other_user = user_factory.create(username='test participant')
        new_participant_data = {'role': BoardParticipant.Role.owner, 'user': other_user.username}

        response = auth_client.put(self.get_url(board.id), self.get_update_data(participants=[new_participant_data]))

        assert response.data == {'participants': [{'role': ['"1" is not a valid choice.']}]}
        assert response.status_code == status.HTTP_400_BAD_REQUEST
