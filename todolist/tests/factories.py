import factory
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import GoalCategory, Board, BoardParticipant, Goal

USER_PASSWORD: str = '123afafa'


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = USER_PASSWORD
    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class DatesModelMixin(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register
class BoardFactory(DatesModelMixin):
    class Meta:
        model = Board

    title = factory.Faker('word')
    is_deleted = False

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = BoardParticipant.Role.owner


@register
class GoalCategoryFactory(DatesModelMixin):
    class Meta:
        model = GoalCategory

    title = 'Test category'
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    is_deleted = False


@register
class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = 'Test goal'
    description = 'Test description'
    due_date = None
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    status = Goal.Status.to_do
    priority = Goal.Priority.medium
