"""
Url mappings for user API.
"""

from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("token/", views.CreateTokenView.as_view(), name="create-token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
