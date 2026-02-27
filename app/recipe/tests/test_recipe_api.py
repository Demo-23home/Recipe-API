"""
Tests for recipe APIs.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


def detail_url(recipe_id):
    """
    create and return a recipe detail URL.
    """
    return reverse("recipe:recipe-detail", args=[recipe_id])


RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    """
    Create and return a sample recipe.
    """

    defaults = {
        "title": "Test recipe title",
        "time_minutes": 4,
        "description": "Test recipe description",
        "price": Decimal(5.50),
        "link": "http://exmaple.com/recipe.pdf",
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeAPITests(TestCase):
    """
    Test unauthenticated recipe API's.
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test an authentication required for recipes list.
        """

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """
    Test Authenticated requests to recipe API's.
    """

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", name="Test User", password="TestPassword@123"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """
        Test retrieving a list of recipes.
        """

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_user_related_recipes(self):
        """
        Test list recipes related to a specific user.
        """

        other_user = get_user_model().objects.create_user(
            email="otheruser@example.com", name="Other User", password="OhterUser@123"
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """
        Test retrieve a recipe by an id
        """

        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)


    def test_create_recipe(self):
        """
        Test creating a recipe.
        """

        payload = {
            "title": "Test Recipe",
            "time_minutes": 4,
            "price": Decimal(5.50)
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=res.data["id"])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

        self.assertEqual(recipe.user, self.user)