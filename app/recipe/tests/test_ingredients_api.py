"""
Tests for Ingredients API.
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import IngredientSerializer

from core.models import Ingredient, Recipe

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def detail_url(ingredient_id):
    """
    Create and return an ingredient detail URL.
    """
    url = reverse("recipe:ingredient-detail", args=[ingredient_id])

    return url


def create_user(email="test@example.com", password="Test@1234"):
    user = get_user_model().objects.create_user(email, password)

    return user


class PublicIngredientAPITests(TestCase):
    """
    Test public Ingredients API endpoints.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test if auth is required for listing ingredients.
        """

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """
    Test Private Ingredients API endpoints.
    """

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """
        Test retrieving a list of ingredients.
        """

        Ingredient.objects.create(user=self.user, name="Ingredient1")
        Ingredient.objects.create(user=self.user, name="Ingredient2")

        ingredients = Ingredient.objects.all().order_by("-name")

        serializer = IngredientSerializer(ingredients, many=True)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_user_ingredients(self):
        """
        Test retrieve ingredients limited to authenticated user.
        """

        user2 = create_user(email="test2@example.com")

        Ingredient.objects.create(name="salt", user=user2)
        ingredient = Ingredient.objects.create(name="pepper", user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(res.data[0]["id"], ingredient.id)

    def test_update_ingredient(self):
        """
        Test update ingredient.
        """

        ingredient = Ingredient.objects.create(user=self.user, name="Cilantro")

        url = detail_url(ingredient.id)

        payload = {"name": "Potato"}

        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload["name"])

    def test_delete_ingredient(self):
        """
        Test delete a ingredient.
        """

        ingredient = Ingredient.objects.create(user=self.user, name="Carrots")
        url = detail_url(ingredient.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.all().exists()
        self.assertFalse(ingredients)

    def test_filter_ingredients_assigned_to_recipe(self):
        """
        Test listing ingredients by those assigned to recipes.
        """
        in1 = Ingredient.objects.create(user=self.user, name="ing1")
        in2 = Ingredient.objects.create(user=self.user, name="in2")

        recipe = Recipe.objects.create(
            user=self.user, title="recipe1", price=Decimal(5.5), time_minutes=3
        )

        recipe.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)

        self.assertIn(res.data, s1)
        self.assertNotIn(res.data, s2)

    def test_filter_ingredients_unique(self):
        """
        Test filtering ingredients returns a unique list.
        """
        in1 = Ingredient.objects.create(user=self.user, name="in1")
        Ingredient.objects.create(user=self.user, name="in2")
        recipe = Recipe.objects.create(
            user=self.user, title="recipe1", time_minutes=4, price=Decimal(29.5)
        )

        recipe.ingredients.add(in1)
        res = self.client.get(INGREDIENTS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)
