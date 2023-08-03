from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    USER = ("user", _("User"))
    ADMIN = ("admin", _("Admin"))


class User(AbstractUser):
    role = models.CharField(max_length=5, choices=UserRoles.choices, default=UserRoles.USER)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
