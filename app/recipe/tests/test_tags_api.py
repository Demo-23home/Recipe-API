"""
Tests for tags api.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


def detail_url(tag_id):
    url = reverse("recipe:tag-detail", args=[tag_id])
    return url


def create_user(email="test@example.com", password="Test@123"):
    """
    Create and return a user.
    """
    user = get_user_model().objects.create_user(email, password)
    return user


class PublicTagsAPITests(TestCase):
    """
    Test Public Tags API endpoints.
    """

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags(self):
        """
        Test retrieve tags for non-authenticated users.
        """

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsTests(TestCase):
    """
    Test Tags API's for authenticated users.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test retrieve tags for authenticated users.
        """

        Tag.objects.create(name="test1", user=self.user)
        Tag.objects.create(name="test2", user=self.user)

        tags = Tag.objects.all().order_by("-name")

        serializer = TagSerializer(tags, many=True)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_user_tags(self):
        """
        Test retrieve tags limited to user.
        """

        user2 = create_user(email="user2@example.com")
        Tag.objects.create(name="test", user=user2)
        tag = Tag.objects.create(name="test2", user=self.user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)
        self.assertEqual(len(res.data), 1)

    def test_update_tag(self):
        """
        Test updating a tag.
        """

        tag = Tag.objects.create(name="after-dinner", user=self.user)

        url = detail_url(tag.id)

        payload = {"name": "Dessert"}

        res = self.client.patch(url, payload)

        tag.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag(self):
        """
        Test Deleting a tag.
        """

        tag = Tag.objects.create(name="break-fast", user=self.user)

        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        tags = Tag.objects.all()

        self.assertFalse(tags.exists())
