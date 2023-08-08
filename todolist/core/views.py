import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserCreateSerializer, UserRetrieveUpdateSerializer, UserPasswordUpdateSerializer


@csrf_exempt
@require_POST
def login_view(request):
    login_data = json.loads(request.body)
    username = login_data.get('username')
    password = login_data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse(login_data, status=201)

    return JsonResponse({'message': 'Invalid login'}, status=401)


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({}, status=204)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserPasswordUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
