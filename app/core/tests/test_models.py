"""
Tests for the models of the core app.
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core.models import (
    image_upload_path,
)


def user_model_data_test() -> dict:
    """Return a dictionary of data for testing the User model."""
    return {
        'email': 'user@example.com',
        'password': 'testpass123',
        'name': 'Test User'
    }


class UserModelTests(TestCase):
    """Tests for the User model."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        data = user_model_data_test()
        user = get_user_model().objects.create_user(**data)

        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        data = user_model_data_test()
        data['email'] = 'example@Gmail.com'
        user = get_user_model().objects.create_user(**data)

        self.assertEqual(user.email, data['email'].lower())

    def test_create_user_same_email_raises_error(self):
        """Test creating a user with the same email raises an error."""
        data = user_model_data_test()
        get_user_model().objects.create_user(**data)
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(**data)

    def test_create_superuser(self):
        """Test creating a new superuser."""
        data = user_model_data_test()
        user = get_user_model().objects.create_superuser(**data)

        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_admin(self):
        """Create admin user."""
        data = user_model_data_test()
        user = get_user_model().objects.create_admin(**data)

        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_staff)

    @patch('core.models.uuid.uuid4')
    def test_upload_image_file_uuid(self, mock_uuid):
        """Test generate image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = image_upload_path(None, 'myimage.jpg')
        exp_path = f'uploads/images/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
