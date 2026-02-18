import os

ENV = os.getenv("DJANGO_ENV", "dev")  # default to dev

if ENV == "prod":
    from .prod import *  # noqa
else:
    from .dev import *  # noqa
