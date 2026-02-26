"""
Tests for user api's
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create-user")
TOKEN_URL = reverse("users:create-token")
ME_URL = reverse("users:me")


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

    def test_create_token_for_user(self):
        """
        Testing if a token is generated when user is logged in.
        """

        user_data = {
            "email": "testemail@example.com",
            "password": "testPassword@123",
            "name": "Test User",
        }

        create_user(**user_data)

        payload = {"email": user_data["email"], "password": user_data["password"]}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        Testing no token is generated if credentials were incorrect.
        """

        create_user(email="testeamil@example.com", password="TestPassword@123")

        payload = {"email": "notAnEmail", "password": "notAPssword"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """
        Testing post a blank password returns an error.
        """

        payload = {"email": "testemail@example.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthenticated(self):
        """
        Test authentication is required for users.
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """
    Test API requests that requires authentication.
    """

    def setUp(self):
        self.user = create_user(
            email="testemail@example.com", password="TestPassword@123", name="Test User"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving user profile for logged in users.
        """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(res.data, {"email": self.user.email, "name": self.user.name})

    def test_post_me_not_allowed(self):
        """
        Test POST method isn't allowed with me endpoint.
        """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating user profile data for authenticated users.
        """

        payload = {"name": "New Name", "password": "NewPassword@123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
