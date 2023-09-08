"""
Serializers for core app
"""
from rest_framework import serializers

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
