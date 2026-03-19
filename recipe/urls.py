from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewset)

app_name = "recipe"


urlpatterns = [
    path("", include(router.urls)),
]
