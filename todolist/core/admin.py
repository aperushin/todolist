from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    ModelAdmin class for User model customizing the displayed fields
    """
    list_display = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': (
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
        )}),
    )
    readonly_fields = ('date_joined', 'last_login')


# admin.site.register(User, CustomUserAdmin)
