from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(max_length=128, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, args: dict) -> dict:
        if self.initial_data['password'] != self.initial_data['password_repeat']:
            raise serializers.ValidationError({'password_repeat': ['Passwords do not match']})

        return args

    def create(self, validated_data: dict) -> User:
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserPasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, validators=[validate_password])
    old_password = serializers.CharField(max_length=128)

    def validate_old_password(self, value: str) -> str:
        if not self.instance.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')

        return value

    def update(self, instance: User, validated_data: dict) -> User:
        self.instance.set_password(validated_data['new_password'])
        self.instance.save()
        return self.instance

    def to_representation(self, instance: User) -> dict:
        return self.validated_data
