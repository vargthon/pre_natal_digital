import datetime
import uuid
import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError


def image_upload_path(instance, filename: str) -> str:
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'images', filename)


def profile_image_upload_path(instance, filename: str) -> str:
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'images', filename)


class UserManager(BaseUserManager):
    """
    Custom User Manager class
    """

    def create_user(self, cpf, password=None, **extra_fields):
        """Create and save a new user"""
        if not cpf:
            raise ValidationError('Users must have an cpf')
        #user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, cpf, password, **extra_fields):
        """Create and save a new superuser"""
        user = self.create_user(cpf, password, **extra_fields)
        user.is_superuser = False
        user.is_staff = True

        user.save(using=self._db)

        return user

    def create_admin(self, cpf, password, **extra_fields):
        """Create and save a new admin"""
        user = self.create_user(cpf, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model class
    """
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True,
                              upload_to=image_upload_path)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'

    def __str__(self):
        return self.cpf


class Address(models.Model):
    """Model for Address"""
    name = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    complement = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    
    
class UserProfile(models.Model):
    """Custom model for user profile"""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True, auto_now=True) 
    image = models.ImageField(
        null=True,
        upload_to=profile_image_upload_path
    )

    def __str__(self):
        return self.user.email
