"""
Views for the core app.
"""
from django.contrib.auth import get_user_model
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.exceptions import PermissionDenied
from core.serializers import UserSerializer

from core import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    Manage users in the database.
    """
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """
        if self.action == 'upload_image':
            return serializers.UserImageSerializer

        return self.serializer_class

    def get_object(self):
        """
        Retrieve the user for the authenticated request.
        """
        if self.request.user.is_staff:
            return super().get_object()
        else:
            if self.request.user.id != int(self.kwargs['pk']):
                raise PermissionDenied(
                    "You don't have permission to access this user.")

        return self.request.user

    def perform_create(self, serializer):
        """
        Create a new user.
        """
        if self.request.user.is_staff:
            return serializer.save()
        else:
            raise PermissionDenied("Only superuser can create users.")

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """
        Upload an image to a user.
        """
        user = self.get_object()
        serializer = self.get_serializer(
            user,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_update(self, serializer):
        """
        Update a user.
        """
        if self.request.user.is_staff:
            return serializer.save()
        else:
            if self.request.user.id == serializer.instance.id:
                return serializer.save()

        raise PermissionDenied("Users only can change their own data.")

    def perform_destroy(self, instance):
        """
        Delete a user.
        """
        if self.request.user.is_superuser or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("Only superuser can delete users.")


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Manage users in the database.
    """
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        """
        Retrieve the user for the authenticated request.
        """
        return super().get_object()

    def perform_create(self, serializer):
        """
        Create a new user.
        """
        if self.request.user.is_staff:
            user = serializer.save()
            user.is_active = True
            return user.save()
        else:
            raise PermissionDenied("Only admin can create admins.")

    def perform_update(self, serializer):
        """
        Update a user.
        """
        if self.request.user.is_staff:
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            return user.save()
        else:
            raise PermissionDenied("Only admin can change admins.")

    def perform_destroy(self, instance):
        """
        Delete a user.
        """
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise PermissionDenied("Only admin can delete admins.")


class MeView(APIView):
    """
    Manage the authenticated user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        """
        Retrieve the authenticated user.
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
