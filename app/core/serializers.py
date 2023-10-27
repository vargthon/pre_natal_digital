"""
Serializers for core app
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from core.models import (
    User,
    UserProfile,
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
                'min_length': 8,
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return User.objects.create_user(**validated_data)


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for user image."""

    class Meta:
        model = User
        fields = (
            'id',
            'image',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'image': {
                'required': True,
            }
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile objects."""
    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'name',
            'phone_number',
            'address',
            'image',
            'user',
        )
        read_only_fields = ('id', 'user',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['admin'] = user.is_staff
        # ...

        return token
