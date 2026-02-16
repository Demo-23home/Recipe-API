"""
Database models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Manager for users.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Crete, save and return a new user.
        """
        if not email:
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system.
    """

    email = models.EmailField(_("Email"), max_length=254, unique=True)
    name = models.CharField(_("Name"), max_length=50)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
