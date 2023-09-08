from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError


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
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

    def create_admin(self, email, password, **extra_fields):
        """Create and save a new admin"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = False

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model class
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
