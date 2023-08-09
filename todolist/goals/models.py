from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import User


class GoalCategory(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    user = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name=_('Deleted'), default=False)
    created = models.DateTimeField(verbose_name=_('Created'))
    updated = models.DateTimeField(verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        """
        Update timestamps on save
        """
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)
