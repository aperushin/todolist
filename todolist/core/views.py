from typing import Any

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.models import User
from core.serializers import (
    UserCreateSerializer, ProfileSerializer, UpdatePasswordSerializer, LoginSerializer,
)


class LoginView(CreateAPIView):
    serializer_class: BaseSerializer = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login(request=request, user=serializer.save())
        return Response(serializer.data)


class UserCreateView(CreateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class: BaseSerializer = UserCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class: BaseSerializer = ProfileSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UpdatePasswordView(UpdateAPIView):
    serializer_class: BaseSerializer = UpdatePasswordSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
