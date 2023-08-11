import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from core.models import User
from goals.models import GoalCategory

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


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = 'Test category title'
    user = factory.SubFactory(UserFactory)
    is_deleted = False
    created = timezone.now()
    updated = timezone.now()
