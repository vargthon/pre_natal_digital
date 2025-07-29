from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from informations.models import (
    Information,
)

def information_model_data_test() -> dict:
    """Return a dictionary of data for testing the Information model."""
    return {
        'title': 'Test Information',
        'description': 'This is a test content for the information model.',
    }
    
def create_information(**params):
    """Helper function to create an Information instance."""
    return Information.objects.create(**params)


class InformationModelTests(TestCase):
    """Tests for the Information model."""

    def test_create_information_successful(self):
        """Test creating a new Information instance is successful."""
        data = information_model_data_test()
        info = create_information(**data)

        self.assertEqual(info.title, data['title'])
        self.assertEqual(info.description, data['description'])

    def test_information_str_method(self):
        """Test the __str__ method of the Information model."""
        data = information_model_data_test()
        info = create_information(**data)

        self.assertEqual(str(info), data['title'])

    def test_information_ordering(self):
        """Test that Information instances are ordered by 'order' field."""
        info1 = create_information(title='First Info', order=1)
        info2 = create_information(title='Second Info', order=2)

        self.assertListEqual(
            list(Information.objects.all()),
            [info1, info2]
        )