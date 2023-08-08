from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class PasswordField(serializers.CharField):
    """
    Password field for serializers

    Automatically appends password validator to validators
    """
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)
