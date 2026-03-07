import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Always attempt to load .env (safe if it doesn't exist)
load_dotenv(BASE_DIR / ".env")

# Now read environment
ENV = os.getenv("DJANGO_ENV", "prod")

if ENV == "dev":
    from .dev import *  # noqa
else:
    from .prod import *  # noqa
