"""
Tests for views (API) of core app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

import tempfile
import os
from PIL import Image as PILImage

from core.models import UserProfile
from core.tests.data_test import (
    USER_DATA_TEST,
    USER_DATA_TEST_SAMPLE,
    SUPERVISOR_DATA_TEST
)

CREATE_USER_URL = reverse('core:user-list')


def detail_url(user_id):
    """
    Return user detail URL.
    """
    return reverse('core:user-upload-image', args=[user_id])


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


def create_admin(**params):
    """
    Helper function to create an admin.
    """
    return get_user_model().objects.create_admin(**params)


class UserApiTests(TestCase):
    """
    Test the users API (public).
    """

    def setUp(self):
        self.user = create_user(**USER_DATA_TEST)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_users_could_not_create_users(self):
        """Test if users could not be created by other users."""
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.post(CREATE_USER_URL, {
            'email': 'newuser@gmail.com',
            'name': 'Test User',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_change_data(self):
        """
        Test that user can change his data.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.logout()
        self.client.force_authenticate(user=user)
        res = self.client.patch(reverse('core:user-detail', args=[user.id]), {
            'name': 'Test User UPDATED',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cannot_change_other_user_data(self):
        """
        Test that user cannot change other user data.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.logout()
        self.client.force_authenticate(user=user)
        res = self.client.patch(
            reverse('core:user-detail', args=[self.user.id]),
            {
                'name': 'Test User UPDATED',
                'password': 'testpass123',
            }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_himself(self):
        """
        Test that user cannot delete himself.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.logout()
        self.client.force_authenticate(user=user)
        res = self.client.delete(
            reverse('core:user-detail', args=[user.id]), format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_data_of_other_user_raise_exception(self):
        """
        Test that user cannot get data of other user.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.get(
            reverse('core:user-detail', args=[self.user.id]), format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_data_of_himself(self):
        """
        Test that user can get data of himself.
        """
        res = self.client.get(
            reverse('core:user-detail', args=[self.user.id]), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cannot_get_other_data(self):
        """
        Test that user cannot get data of other user.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.get(
            reverse('core:user-detail', args=[self.user.id]), format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_new_user(self):
        """
        Test that user cannot create new user.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.post(CREATE_USER_URL, {
            'email': 'exampl@gmail.com',
            'name': 'Test User22',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_cannot_create_supervisors(self):
        """
        Test that user cannot create supervisor.
        """
        res = self.client.post(
            CREATE_USER_URL,
            SUPERVISOR_DATA_TEST,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class SupervisorApiTest(TestCase):
    """
    Test the supervisor API (public).
    """

    def setUp(self):
        self.user = create_superuser(**USER_DATA_TEST)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_valid_supervisor_success(self):
        """
        Test creating supervisor with valid payload is successful.
        """
        res = self.client.post(
            reverse('core:user-list'),
            SUPERVISOR_DATA_TEST,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_successfull(self):
        """
        Test creating user with valid payload is successful.
        """
        res = self.client.post(
            reverse('core:user-list'),
            USER_DATA_TEST_SAMPLE,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_exist_user_fail(self):
        """
        Test creating user that already exists fails.
        """
        res = self.client.post(
            reverse('core:user-list'),
            USER_DATA_TEST,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_exist_supervisor_fail(self):
        """
        Test creating supervisor that already exists fails.
        supervisor already exist if e-mail is the same.
        """
        res = self.client.post(
            reverse('core:user-list'),
            SUPERVISOR_DATA_TEST,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(
            reverse('core:user-list'),
            SUPERVISOR_DATA_TEST,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password_fail(self):
        """
        Test creating user with password that is too short fails.
        """
        res = self.client.post(
            reverse('core:user-list'),
            {
                'email': 'test2@gmail.com',
                'name': 'Test',
                'password': '123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_email_fail(self):
        """
        Test creating user with invalid email fails.
        """
        res = self.client.post(
            reverse('core:user-list'),
            {
                'name': 'Test',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supervisor_sucessfull(self):
        """
        Test creating supervisor with valid payload is successful.
        """
        res = self.client.post(
            reverse('core:user-list'),
            SUPERVISOR_DATA_TEST,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_user(self):
        """
        Test deleting user.
        """
        res = self.client.post(
            reverse('core:user-list'),
            USER_DATA_TEST_SAMPLE,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(
            email=USER_DATA_TEST_SAMPLE['email'])
        res = self.client.delete(
            reverse('core:user-detail', args=[user.id]),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        """
        Test updating user.
        """
        res = self.client.post(
            reverse('core:user-list'),
            USER_DATA_TEST_SAMPLE,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(
            email=USER_DATA_TEST_SAMPLE['email'])
        res = self.client.patch(
            reverse('core:user-detail', args=[user.id]),
            {
                'name': 'Test User UPDATED', },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Test User UPDATED')


class AdminApiTest(TestCase):
    """
    Tests for Admin User API
    """

    def setUp(self):
        self.admin_user = create_admin(**USER_DATA_TEST)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_create_valid_admin_success(self):
        """
        Test creating admin with valid payload is successful.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'adminuser@gmail.com',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_exist_admin_fail(self):
        """
        Test creating admin that already exists fails.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_admin_with_short_password_fail(self):
        """
        Test creating admin with password that is too short fails.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'emailadmin@gmail.com',
                'name': 'Test Admin',
                'password': '123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_admin_with_invalid_email_fail(self):
        """
        Test creating admin with invalid email fails.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'emailadmin',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_admin(self):
        """
        Test deleting admin.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'adminnewuser@gmail.com',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['id'])
        res = self.client.delete(
            reverse('core:admin-user-detail', args=[user.id]),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_admin(self):
        """
        Test updating admin.
        """
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'adminnewuser@gmail.com',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['id'])
        res = self.client.patch(
            reverse('core:admin-user-detail', args=[user.id]),
            {
                'name': 'Test Admin UPDATED',
                'password': 'testpass123',
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_cannot_create_admin(self):
        """
        Test that user cannot create admin.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'adminusertotest@gmail.com',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_delete_admin(self):
        """
        Test that user cannot update or delete admin.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.delete(
            reverse('core:admin-user-detail', args=[self.admin_user.id]),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_admin(self):
        """
        Test that user cannot update admin.
        """
        user = create_user(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.patch(
            reverse('core:admin-user-detail', args=[self.admin_user.id]),
            {
                'name': 'Test Admin UPDATED', },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_cannot_delete_admin(self):
        """
        Test that supervisor cannot delete admin.
        """
        user = create_superuser(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.delete(
            reverse('core:admin-user-detail', args=[self.admin_user.id]),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticationApiTest(TestCase):
    """
    Tests for Authentication API
    """

    def setUp(self):
        self.user = create_superuser(**USER_DATA_TEST)
        self.client = APIClient()

    def test_login_success(self):
        """
        Test login success.
        """
        res = self.client.post(
            reverse('core:token'),
            {
                'email': USER_DATA_TEST['email'],
                'password': USER_DATA_TEST['password']
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        """
        Test login fail.
        """
        res = self.client.post(
            reverse('core:token'),
            {
                'email': USER_DATA_TEST['email'],
                'password': 'wrongpassword'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        """
        Test refresh token success.
        """
        res = self.client.post(
            reverse('core:token'),
            {
                'email': USER_DATA_TEST['email'],
                'password': USER_DATA_TEST['password']
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            reverse('core:refresh-token'),
            {
                'refresh': res.data['refresh']
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token_fail(self):
        """
        Test refresh token fail.
        """
        res = self.client.post(
            reverse('core:refresh-token'),
            {
                'refresh': 'wrongrefresh'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_token_success(self):
        """
        Test verify token success.
        """
        res = self.client.post(
            reverse('core:token'),
            {
                'email': USER_DATA_TEST['email'],
                'password': USER_DATA_TEST['password']
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            reverse('core:verify-token'),
            {
                'token': res.data['access']
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class UserUploadImageTest(TestCase):
    """Tests for Image Upload API."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(**USER_DATA_TEST)
        self.client.force_authenticate(self.user)
        return super().setUp()

    def tearDown(self) -> None:
        self.user.delete()
        return super().tearDown()

    def test_upload_user_image(self):
        """Test for upload image to user."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            image = PILImage.new('RGB', (10, 10))
            image.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                detail_url(self.user.id), {'image': ntf}, format='multipart')
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.user.image.path))

    def test_upload_user_image_invalid(self):
        """Test for upload invalid image to user."""
        res = self.client.post(
            detail_url(self.user.id),
            {'image': 'notimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


PROFILE_TEST_DATA = {
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
        'birth_date': '2021-01-01',
        'image': None
    }


def user_profile_detail_url(profile_id):
    """
    Return user profile detail URL.
    """
    return reverse('core:user-profile-detail', args=[profile_id])


class UserProfileAdminTest(TestCase):
    """Tests for User Profile"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(**USER_DATA_TEST)
        self.client.force_authenticate(self.user)
        return super().setUp()

    def test_profile_create(self):
        """Test successfull create user profile"""
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], PROFILE_TEST_DATA['name'])
        self.assertEqual(res.data['phone_number'],
                         PROFILE_TEST_DATA['phone_number'])
        self.assertEqual(res.data['image'], PROFILE_TEST_DATA['image'])

    def test_create_duplicate_profile_fail(self):
        """Test fail create duplicate profile"""
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_raise_401_with_not_logged(self):
        """Should raise error unauthorized if user not logged"""
        self.client.logout()
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_logic_delete_profile(self):
        """Delete should logically delete profile"""
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_profile = UserProfile.objects.get(pk=res.data['id'])

        res = self.client.delete(
            user_profile_detail_url(created_profile.id),
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        created_profile.refresh_from_db()
        self.assertFalse(created_profile.deleted_at is None)

    def test_should_permit_user_destroy(self):
        """Delete user should not delete profile too."""
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_profile = UserProfile.objects.get(pk=res.data['id'])

        user = created_profile.user
        user.delete()
        created_profile.refresh_from_db()

        self.assertTrue(created_profile.user is None)

    def test_should_update_profile_successfully(self):
        """Should update user profile"""
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_profile = UserProfile.objects.get(pk=res.data['id'])

        res = self.client.patch(
            user_profile_detail_url(created_profile.id),
            {
                'name': 'Test User UPDATED',
                'phone_number': '987654321',
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        created_profile.refresh_from_db()
        self.assertEqual(created_profile.name, 'Test User UPDATED')
        self.assertEqual(created_profile.phone_number, '987654321')

    def test_raise_unauthorized_profile_update(self):
        """Should raise 401 unauthorized when try to
        update other user profile."""
        user = create_user(**{
            'email': 'otheruser@gmail.com',
            'name': 'Other User',
            'password': 'testpass123'
        })
        self.client.force_authenticate(user=user)
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_profile = UserProfile.objects.get(pk=res.data['id'])

        self.client.logout()
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(
            user_profile_detail_url(created_profile.id),
            {
                'name': 'Test User UPDATED',
                'phone_number': '987654321',
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_update_profile_without_pk(self):
        """
        Test if partial update is successful.
        """
        res = self.client.post(
            reverse('core:user-profile-list'),
            PROFILE_TEST_DATA,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_profile = UserProfile.objects.get(pk=res.data['id'])

        res = self.client.post(
            reverse('core:user-profile-update'),
            {
                'name': 'Test User UPDATED',
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        created_profile.refresh_from_db()
        self.assertEqual(created_profile.name, 'Test User UPDATED')


def upload_user_profile_url(profile_id):
    """
    Return upload user profile image URL.
    """
    return reverse('core:user-profile-upload-image', args=[profile_id])


def create_user_profile(**params):
    """
    Helper function to create a user profile.
    """
    return UserProfile.objects.create(**params)


def upload_image_url():
    """
    Return upload image URL.
    """
    return reverse('core:image-upload')


class UploadUserProfileImage(TestCase):
    """Tests for upload image API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(**USER_DATA_TEST)
        self.user_profile = create_user_profile(
            **PROFILE_TEST_DATA, user=self.user)
        self.client.force_authenticate(self.user)
        return super().setUp()

    def test_upload_user_profile_image(self):
        """Test for upload image to user profile."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            image = PILImage.new('RGB', (10, 10))
            image.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                upload_image_url(),
                {'image': ntf}, format='multipart')
        self.user_profile.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.user_profile.image.path))

    def test_upload_user_profile_image_invalid(self):
        """Test for upload invalid image to user profile."""
        res = self.client.post(
            upload_image_url(),
            {'image': 'notimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
