import factory
from django.contrib.auth.hashers import make_password

from core.models import User, UserRoles

USER_PASSWORD = '123afafa'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = make_password(USER_PASSWORD)
    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    role = UserRoles.USER
    is_active = True
