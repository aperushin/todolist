from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import User


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


class GoalCategory(DatesModelMixin):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name=_('Deleted'), default=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Goal(DatesModelMixin):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    due_date = models.DateField(verbose_name=_('Due date'), null=True)
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name=_('Category'), on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name=_('Status'), choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'),
        choices=Priority.choices,
        default=Priority.medium
    )

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
