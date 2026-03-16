# app/app/settings/prod.py
from .base import *  # noqa — must come first
import os
import dj_database_url

DEBUG = True

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
