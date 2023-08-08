from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from core.models import User
from core.fields import PasswordField


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data: dict) -> User:
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        if not user:
            raise AuthenticationFailed
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, args: dict) -> dict:
        if self.initial_data['password'] != self.initial_data['password_repeat']:
            raise serializers.ValidationError({'password_repeat': ['Passwords do not match']})
        return args

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    new_password = PasswordField(required=True)
    old_password = PasswordField(required=True)

    def validate_old_password(self, old_password: str) -> str:
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError('Old password is incorrect')
        return old_password

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
