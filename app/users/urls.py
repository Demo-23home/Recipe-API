"""
Url mappings for user API.
"""

from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("tpken/", views.CreateTokenView.as_view(), name="create-token"),
]
