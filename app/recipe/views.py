"""
Views for recipe API.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
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

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        """
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Manage Tags in DB.
    """

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        Filter querysets to authenticated users.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")
