import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from core.models import User
from goals.models import GoalCategory, Board, BoardParticipant, Goal

USER_PASSWORD = '123afafa'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = make_password(USER_PASSWORD)
    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    is_active = True


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('word')
    is_deleted = False
    created = timezone.now()
    updated = timezone.now()


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = BoardParticipant.Role.owner


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = 'Test category title'
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    is_deleted = False
    created = timezone.now()
    updated = timezone.now()


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker('word')
    description = 'Test description'
    due_date = None
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    status = Goal.Status.to_do
    priority = Goal.Priority.medium
