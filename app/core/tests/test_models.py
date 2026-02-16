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

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_user_normalized_email(self):
        """
        Test email is normalized for new users.
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "test2@example.com"],
            ["TEST3@EXAMPLE.COM", "test3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "TestPassword@123")

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test that creating a user without email raises a Value Error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "TestPassword@123")

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "TestPassword@123"
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
