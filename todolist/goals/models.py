from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from core.models import User


class DatesModelMixin(models.Model):
    created = models.DateTimeField(verbose_name=_('Created'))
    updated = models.DateTimeField(verbose_name=_('Updated'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        """
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DatesModelMixin):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    is_deleted = models.BooleanField(verbose_name=_('Deleted'), default=False)

    def __str__(self):
        return f'Board {self.id}: {self.title}'

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')


class BoardParticipant(DatesModelMixin):
    class Role(models.IntegerChoices):
        owner = 1, _('Owner')
        writer = 2, _('Writer')
        reader = 3, _('Reader')

        @classmethod
        @property
        def editable_choices(cls) -> list[tuple, tuple]:
            return [(member.value, member.label) for member in cls if member != cls.owner]

    board = models.ForeignKey(Board, verbose_name=_('Board'), on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name=_('Role'), choices=Role.choices, default=Role.owner)

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')


class GoalCategory(DatesModelMixin):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    board = models.ForeignKey(Board, verbose_name=_('Board'), on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name=_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Goal(DatesModelMixin):
    class Status(models.IntegerChoices):
        to_do = 1, _('To do')
        in_progress = 2, _('In progress')
        done = 3, _('Done')
        archived = 4, _('Archived')

    class Priority(models.IntegerChoices):
        low = 1, _('Low')
        medium = 2, _('Medium')
        high = 3, _('High')
        critical = 4, _('Critical')

    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    due_date = models.DateField(verbose_name=_('Due date'), null=True)
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    category = models.ForeignKey(
        to=GoalCategory, verbose_name=_('Category'), on_delete=models.PROTECT, related_name='goals'
    )
    status = models.PositiveSmallIntegerField(verbose_name=_('Status'), choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'), choices=Priority.choices, default=Priority.medium
    )

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')


class GoalComment(DatesModelMixin):
    text = models.TextField(verbose_name=_('Text'), validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name=_('Goal'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
