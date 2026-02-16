"""
Django command to make sure PostgreSQL is available.
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait for database to be available"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (OperationalError, Psycopg2OpError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        # Optional small pause to ensure DB is fully ready
        time.sleep(2)
        self.stdout.write(self.style.SUCCESS("Database available!"))
