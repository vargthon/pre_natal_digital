"""
Serializers for core app
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from core.models import (
    User
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'name',
            'is_active',
            'is_staff',
            'is_superuser'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            }
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['admin'] = user.is_staff
        # ...

        return token
