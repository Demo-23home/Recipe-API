"""
Serializers for recipe API's.
"""

from core.models import Recipe

from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "user", "title", "description", "time_minutes", "price", "link"]
        read_only_fields = ["id", "user"]


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
