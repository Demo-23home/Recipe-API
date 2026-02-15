"""
Django command to make sure PostgreSQL is available.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for DB
    """

    def handle(self, *args, **options):
        pass
