from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    search_fields = ('chat_id', 'user__username')
