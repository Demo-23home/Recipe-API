"""
Serializers for recipe API's.
"""

from core.models import Recipe, Tag, Ingredient

from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "user"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    # by default nested serializer are read only.
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "user", "title", "time_minutes", "price", "tags"]
        read_only_fields = ["id", "user"]

    def _create_or_update(self, tags, recipe):
        """
        Create or update tags on recipe if needed.
        """
        auth_user = self.context["request"].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """
        Create the recipe with tags.
        """
        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)

        self._create_or_update(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)

        if tags is not None:
            instance.tags.clear()
            self._create_or_update(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description", "link"]
