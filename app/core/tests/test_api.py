"""
Tests for views (API) of core app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


from core.tests.data_test import (
    USER_DATA_TEST,
    USER_DATA_TEST_SAMPLE,
    SUPERVISOR_DATA_TEST
)

CREATE_USER_URL = reverse('core:user-list')


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
        })
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
                'name': 'Test Admin UPDATED', },
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

    def test_supervisor_cannot_create_admin(self):
        """
        Test that supervisor cannot create admin.
        """
        user = create_superuser(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'admintestcreate@gmail.com',
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

    def test_supervisor_cannot_update_admin(self):
        """
        Test that supervisor cannot update admin.
        """
        user = create_superuser(**USER_DATA_TEST_SAMPLE)
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

    def test_supervisor_cannot_create_admin_users(self):
        """
        Test that supervisor cannot create admin.
        """
        user = create_superuser(**USER_DATA_TEST_SAMPLE)
        self.client.force_authenticate(user=user)
        res = self.client.post(
            reverse('core:admin-user-list'),
            {
                'email': 'adminnewuser@gmail.com',
                'name': 'Test Admin',
                'password': 'testpass123'
            },
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
