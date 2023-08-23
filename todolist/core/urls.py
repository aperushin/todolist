from django.urls import path

from core.views import UserCreateView, LoginView, ProfileView, UpdatePasswordView

app_name = 'core'

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update-password'),
]
