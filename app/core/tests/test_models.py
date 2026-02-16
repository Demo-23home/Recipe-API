"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    Test models.
    """

    def test_create_user_model_with_email(self):
        """
        Test creating user model with email is successful.
        """
        email = "testEamil@example.com"
        password = "TestPassword@123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
