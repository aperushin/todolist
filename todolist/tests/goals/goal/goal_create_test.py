import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User


@pytest.mark.django_db
class TestCreateGoal:
    url: str = reverse('goals:create-goal')
    default_due_date: str = '2124-12-12'

    def get_creation_data(self, **kwargs) -> dict:
        data = {
            'title': 'Test goal',
            'description': 'Test description',
            'due_date': self.default_due_date,
            'status': 1,
            'priority': 1
        }
        data |= kwargs
        return data

    def test_success(self, auth_client, goal_category, goal_data):
        """Test successful goal creation"""
        response = auth_client.post(self.url, self.get_creation_data(category=goal_category.id))

        assert response.data == goal_data(category=goal_category.id, due_date=self.default_due_date)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_goal_deleted_category(self, auth_client, user: User, goal_category_factory):
        """Request with a deleted category returns an error"""
        category = goal_category_factory.create(user=user, is_deleted=True)

        response = auth_client.post(self.url, self.get_creation_data(category=category.id))

        assert response.data == {'category': ['Cannot use a deleted category']}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_goal_not_category_owner(self, auth_client, user_factory, goal_category_factory):
        """Request with a different user's category returns an error"""
        other_user = user_factory.create()
        category = goal_category_factory.create(user=other_user)

        response = auth_client.post(self.url, self.get_creation_data(category=category.id))

        assert response.data == {'category': ['Not an owner of this category']}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_goal_not_authenticated(self, client):
        """Request without authentication returns an error"""
        response = client.post(self.url, self.get_creation_data(category=1))

        assert response.data == {'detail': 'Authentication credentials were not provided.'}
        assert response.status_code == status.HTTP_403_FORBIDDEN
