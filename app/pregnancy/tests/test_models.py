from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from pregnancy.models import PregnantWoman, Address, EmergencyContact


def address_model_test() -> dict:
    """
    Return dictionary of data for test Address Model.
    """
    return {
        'street': 'Test Street',
        'reference_point': 'Test Reference',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345678'
    }

def emergency_contact_model_test() -> dict:
    """
    Return dictionary of data for test Emergency Contact Model.
    """
    return {
        'name': 'Test Name',
        'phone_number': '99999999999',
        'relationship': 'Test Relationship'
    }

def create_address(**params):
    """
    Helper function to create an address.
    """
    return Address.objects.create(**params)

def create_emergency_contact(**params):
    """
    Helper function to create an emergency contact.
    """
    return EmergencyContact.objects.create(**params)

def pregnancy_model_test() -> dict:
    """
    Return dictionary of data for test Pregnancy Model.
    """
    return {
        'full_name': 'Test User',
        'birth_date': '2021-01-01',
        'sus_card_number': '12345678901234567890',
        'nis_number': '123456789012',
        'prefered_name': 'Test Prefer',
        'race': 'Test',
        'ethnicity': 'Test',
        'work_outside_home': False,
        'occupation': 'Test Occupation',
        'mobile_phone': '999999999999',
        'email': 'pregnancy@gmail.com',
        'due_date': '2021-01-01'      
    }

def user_model_data_test() -> dict:
    """
    Return a dictionary of data for testing the User model.
    """
    return {
        'email': 'pregnancy@gmail.com',
        'password': 'testpass123',
        'name': 'Test User'
    }
    
def create_pregnant_woman(**params):
    """
    Helper function to create a pregnancy.
    """
    return PregnantWoman.objects.create(**params)

def create_user(**params):
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(**params)

class PregnancyModelTest(TestCase):
    """
    Test the Pregnancy Model.
    """
    def test_create_pregnant_woman(self):
        """
        Test creating
        """
        address = create_address(**address_model_test())
        emergency_contact = create_emergency_contact(**emergency_contact_model_test())
        data = pregnancy_model_test()
        pregnant_woman = create_pregnant_woman(
            **data,
            address=address,
            emergency_contact=emergency_contact)
        self.assertEqual(pregnant_woman.full_name, data['full_name'])
        