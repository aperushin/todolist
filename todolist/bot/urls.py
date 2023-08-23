from django.urls import path

from bot.views import BotVerifyView

app_name = 'bot'

urlpatterns = [
    path('verify', BotVerifyView.as_view(), name='verify-telegram-user')
]
