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

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValidationError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = False
        user.is_staff = True

        user.save(using=self._db)

        return user

    def create_admin(self, email, password, **extra_fields):
        """Create and save a new admin"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model class
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True,
                              upload_to=image_upload_path)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


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
    phone_number = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    full_name = models.CharField(max_length=255)
    sus_card_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    nis_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    prefered_name = models.CharField(max_length=255, blank=True, null=True)
    race = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    work_outside_home = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)    
    image = models.ImageField(
        null=True,
        upload_to=profile_image_upload_path
    )

    def __str__(self):
        return self.user.email
