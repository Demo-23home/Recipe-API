import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Now read environment
ENV = os.getenv("DJANGO_ENV", "prod")

if ENV == "dev":
    from .dev import *  # noqa
else:
    from .prod import *  # noqa
