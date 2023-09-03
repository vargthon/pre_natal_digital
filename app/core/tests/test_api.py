"""
Tests for views (API) of core app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.urls import reverse
from rest_framework.test import APIClient
# from rest_framework import status


def create_user(**params):
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    """
    Helper function to create a superuser.
    """
    return get_user_model().objects.create_superuser(**params)


class UserApiTests(TestCase):
    """
    Test the users API (public).
    """

    def setUp(self):
        self.client = APIClient()

    def test_user_change_data(self):
        """
        Test that user can change his data.
        """
        pass

    def test_user_cannot_change_other_user_data(self):
        """
        Test that user cannot change other user data.
        """
        pass

    def test_user_cannot_delete_himself(self):
        """
        Test that user cannot delete himself.
        """
        pass

    def test_get_data_of_other_user_raise_exception(self):
        """
        Test that user cannot get data of other user.
        """
        pass

    def test_get_data_of_himself(self):
        """
        Test that user can get data of himself.
        """
        pass

    def test_user_cannot_create_new_user(self):
        """
        Test that user cannot create new user.
        """
        pass


class SupervisorApiTest(TestCase):
    """
    Test the supervisor API (public).
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_supervisor_success(self):
        """
        Test creating supervisor with valid payload is successful.
        """
        pass

    def test_create_user_successfull(self):
        """
        Test creating user with valid payload is successful.
        """
        pass

    def test_create_exist_user_fail(self):
        """
        Test creating user that already exists fails.
        """
        pass

    def test_create_exist_supervisor_fail(self):
        """
        Test creating supervisor that already exists fails.
        supervisor already exist if e-mail is the same.
        """
        pass

    def test_create_user_with_short_password_fail(self):
        """
        Test creating user with password that is too short fails.
        """
        pass

    def test_create_user_with_invalid_email_fail(self):
        """
        Test creating user with invalid email fails.
        """
        pass

    def test_delete_user(self):
        """
        Test deleting user.
        """
        pass

    def test_update_user(self):
        """
        Test updating user.
        """
        pass
