from django.urls import path

from bot.views import BotVerifyView

urlpatterns = [
    path('verify', BotVerifyView.as_view(), name='verify-telegram-user')
]
