"""
Tests for admin page.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """
    Tests for admin site.
    """

    def setUp(self):
        """
        Create users, client
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            "admin@example.com", "TestPassword@123"
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            "user@example.com", "TestPassword@123"
        )

    def test_users_list(self):
        """
        Test that users exist on the list page.
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_edit_page(self):
        """
        Test that user edit admin page works.
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
