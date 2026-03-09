"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="TestPassword@123"):
    """
    Create a user in the system.
    """
    user = get_user_model().objects.create_user(email, password)
    return user


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

        user = create_user(email=email, password=password)

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
            user = create_user(email, "TestPassword@123")

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test that creating a user without email raises a Value Error
        """
        with self.assertRaises(ValueError):
            create_user("", "TestPassword@123")

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """

        user = get_user_model().objects.create_superuser(
            "test@example.com", "TestPassword@123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """
        Test create recipe is successful.
        """

        user = create_user(
            email="testemail@exmaple.com",
            password="TestPassword@123",
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Test Recipe",
            time_minutes=5,
            price=Decimal(5.50),
            description="Simple recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """
        Test creating a tag is successful.
        """
        user = create_user()

        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertTrue(str(tag), tag.name)

    def test_create_ingredient(self):
        """
        Test create Ingredient object.
        """

        user = create_user()
        ingredient = models.Ingredient.objects.create(user=user, name="Tomato")

        self.assertEqual(str(ingredient), ingredient.name)


    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        Test generating iamge path. 
        """
        uuid = "test-uuid"
        mock_uuid.return_value = uuid

        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
