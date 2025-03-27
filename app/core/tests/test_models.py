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
from core.models import UserProfile


def user_model_data_test() -> dict:
    """Return a dictionary of data for testing the User model."""
    return {
        'email': 'user@example.com',
        'password': 'testpass123',
        'name': 'Test User'
    }
    
def address_model_data_test() -> dict:
    """Return a dictionary of data for testing the Address model."""
    return {
        'name': 'Test Address',
        'street': 'Test location',
        'city': 'Test city',
        'state': 'Test state',
        'cep': '99999999',
        'complement': 'Test complement',
    }


def user_profile_model_data_test() -> dict:
    """Return a dictionary of data for testing the UserProfile model."""
    return {
        'name': 'Test bio',
        'phone_number': '999999999999',
        'full_name': 'Test Full Name',
        'sus_card_number': '99999999999999999999',
        'nis_number': '99999999999999999999',
        'birth_date': '2021-01-01',
        'prefered_name': 'Test Preferred Name',
        'race': 'CAUCASIAN',
        'ethnicity': 'WHITE',
        'work_outside_home': False,
        'occupation': 'Test Occupation',
        'mobile_phone': '999999999999',
        'email': 'test@gmail.com',
        'due_date': '2021-01-01',
    }


def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)


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
        self.assertTrue(user.is_staff)

    @patch('core.models.uuid.uuid4')
    def test_upload_image_file_uuid(self, mock_uuid):
        """Test generate image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = image_upload_path(None, 'myimage.jpg')
        exp_path = f'uploads/images/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)


class UserProfileModelTest(TestCase):
    """Tests for user profile model."""

    def setUp(self) -> None:
        self.user = create_user(**user_model_data_test())
        return super().setUp()

    def test_create_user_profile(self):
        """Test create user profile."""
        data = user_profile_model_data_test()
        profile = UserProfile.objects.create(user=self.user, **data)
        profile.name = data['name']
        profile.phone_number = data['phone_number']
        profile.save()

        self.assertEqual(profile.name, data['name'])
        self.assertEqual(profile.phone_number, data['phone_number'])
