"""
Tests for recipe APIs.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


def detail_url(recipe_id):
    """
    create and return a recipe detail URL.
    """
    return reverse("recipe:recipe-detail", args=[recipe_id])


RECIPES_URL = reverse("recipe:recipe-list")


def create_user(**params):
    """
    Create an return a user.
    """
    user = get_user_model().objects.create_user(**params)

    return user


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

        self.user = create_user(email="user@example.com", password="TestPassword@123")

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

        other_user = create_user(email="otheruser@example.com", password="User@123")

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

        payload = {"title": "Test Recipe", "time_minutes": 4, "price": Decimal(5.50)}

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

        self.assertEqual(recipe.user, self.user)

    def test_partial_recipe_update(self):
        """
        Test partial update on recipe object.
        """
        original_link = "http://example.com/recipe.pdf"

        recipe = create_recipe(
            user=self.user, title="Recipe Test Title", link=original_link
        )

        payload = {"title": "New recipe title"}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_recipe_update(self):
        """
        Test full update of recipe.
        """

        recipe = create_recipe(
            user=self.user,
            title="Recipe Test Title",
            link="http://exmpale.com/recipe.pdf",
            description="Short recipe description.",
        )

        payload = {
            "title": "Updated recipe title",
            "link": "http://exmaple.com/new_recipe.pdf",
            "description": "Updated recipe description.",
            "time_minutes": 10,
            "price": "5.33",
        }

        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        for key, value in payload.items():
            actual_value = getattr(recipe, key)
            if isinstance(actual_value, Decimal):
                value = Decimal(str(value))
            self.assertEqual(actual_value, value)

        self.assertEqual(recipe.user, self.user)

    def test_update_recipe_user_fails(self):
        """
        Test updating recipe's user returns and error.
        """

        new_user = create_user(email="newuser@example.com", password="Test@21243")

        recipe = create_recipe(user=self.user)

        payload = {"user": new_user}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        recipe_exists = Recipe.objects.filter(id=recipe.id).exists()

        self.assertFalse(recipe_exists)

    def test_delete_other_user_recipe_error(self):
        """
        Test that user can't delete other users recipes.
        """
        new_user = create_user(email="newuser@example.com", password="Test@21243")

        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        recipe_exists = Recipe.objects.filter(id=recipe.id).exists()

        self.assertTrue(recipe_exists)

    def test_create_recipe_with_tags(self):
        """
        Test creating a recipe with new tags.
        """

        payload = {
            "title": "Test Recipe",
            "time_minutes": 4,
            "price": Decimal(5.50),
            "tags": [{"name": "Thai"}, {"name": "Dinner"}],
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)

        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload["tags"]:
            self.assertTrue(
                exists=recipe.tags.filter(name=tag["name"], user=self.user).exists()
            )

        self.assertEqual(recipe.user, self.user)

    def test_create_recipe_with_existing_tag(self):
        """
        Test create a recipe with a new and an existing tags.
        """
        egyptian_tag = Tag.objects.create(name="Egyptian", user=self.user)

        payload = {
            "title": "Test Recipe",
            "time_minutes": 4,
            "price": Decimal(5.50),
            "tags": [{"name": "Egyptian"}, {"name": "Dinner"}],
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)

        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(egyptian_tag, recipe.tags.all())

        for tag in payload["tags"]:
            self.assertTrue(
                exists=recipe.tags.filter(name=tag["name"], user=self.user).exists()
            )