import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import ANY

from core.models import User
from goals.models import BoardParticipant


@pytest.mark.django_db
class TestListCategory:
    url = reverse('goals:category-list')

    def test_pagination(
            self, auth_client, user: User,  board_participant: BoardParticipant, goal_category_factory
    ):
        """Pagination works correctly"""
        category_count = 5
        goal_category_factory.create_batch(size=category_count, user=user, board=board_participant.board)
        expected_response = {
            'count': category_count,
            'next': None,
            'previous': None,
            'results': ANY,
        }

        response = auth_client.get(reverse('goals:category-list'), data={'limit': 10})

        assert response.data == expected_response
        assert response.status_code == status.HTTP_200_OK

    def test_deleted_not_shown(
            self, auth_client, user: User,  board_participant: BoardParticipant, goal_category_factory
    ):
        """Deleted categories are not shown"""
        category_count = 5
        goal_category_factory.create_batch(size=category_count, user=user, board=board_participant.board)
        goal_category_factory.create(user=user, is_deleted=True)

        response = auth_client.get(reverse('goals:category-list'), data={'limit': 10})
        results = response.data.pop('results')

        assert len(results) == category_count
        assert not any([cat['is_deleted'] for cat in results])
