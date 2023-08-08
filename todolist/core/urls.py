from django.urls import path

from core.views import UserCreateView, login_view, UserRetrieveUpdateDestroyView, UserPasswordUpdateView

urlpatterns = [
    path('signup', UserCreateView.as_view()),
    path('login', login_view),
    path('profile', UserRetrieveUpdateDestroyView.as_view()),
    path('update_password', UserPasswordUpdateView.as_view()),
]
