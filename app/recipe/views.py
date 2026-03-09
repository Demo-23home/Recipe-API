"""
Views for recipe API.
"""

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Ingredient, Recipe, Tag
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Viewsets to manage recipe API's
    """

    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        retrieve recipes for authenticated users.
        """
        recipes = self.queryset.filter(user=self.request.user).order_by("-id")
        return recipes

    def get_serializer_class(self):
        """
        Return serializer based on the request.
        """
        if self.action == "list":
            return serializers.RecipeSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        """
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """
        Upload an image to recipe.
        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewset(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Base class for Recipe Ingredients, Tag viewsets.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter querysets to authenticated users.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewset):
    """
    Manage Tags in DB.
    """

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewset(BaseRecipeAttrViewset):
    """
    Manage Ingredients in DB.
    """

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
