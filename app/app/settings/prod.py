import dj_database_url
import os

DEBUG = False

DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

ALLOWED_HOSTS = ["*"]
