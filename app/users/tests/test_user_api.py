"""
Tests for user api's
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create-user")


def create_user(**params):
    """
    Create and return a new user.
    """
    return get_user_model().objects.create_user(**params)


class PublicAPIUserTests(TestCase):
    """
    Test the public features of the user API.
    """

    def setUp(self):
        self.client = APIClient()
        return

    def test_create_user_success(self):
        """
        Testing create user successfully.
        """

        payload = {
            "name": "Test User",
            "password": "TestPassword@123",
            "email": "testuser@example.com",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.email, payload["email"])
        self.assertNotIn("password", res.data)

    def test_user_with_existing_email_error(self):
        """
        Test error returned if user email exists.
        """

        payload = {
            "name": "Test User",
            "password": "TestPassword@123",
            "email": "testser@example.com",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Test error returned if user password is too short.
        """
        payload = {
            "name": "Test User",
            "password": "123",
            "email": "testuser@example.com",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)


