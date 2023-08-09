from pytest_factoryboy import register

from tests.factories import UserFactory, GoalCategoryFactory

register(UserFactory)
register(GoalCategoryFactory)
