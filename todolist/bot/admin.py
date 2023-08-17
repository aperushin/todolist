from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('tg_chat_id', 'user')
    search_fields = ('tg_chat_id', 'user__username')
