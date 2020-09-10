from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe

class TagSerializer(serializers.ModelSerializer):
	"""Serializser for tag objects"""

	class Meta:
		model = Tag
		fields = ('id', 'name')
		read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
	"""Serializer for ingredient objects"""

	class Meta:
		model = Ingredient
		fields = ('id', 'name')
		read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
	"""Serializser a recipe"""
	# PrimaryKeyRelatedField used to just to show id of related tables
	ingredients = serializers.PrimaryKeyRelatedField(
		many=True,
		queryset=Ingredient.objects.all()
		)
	tags = serializers.PrimaryKeyRelatedField(
		many=True,
		queryset=Tag.objects.all()
		)

	class Meta:
		model = Recipe
		fields = (
			'id','title', 'ingredients', 'tags', 'time_minutes',
			'price', 'link'
			)
		read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
	"""Serialize a recipe detail"""
	# many=True used to show detail of related serializers
	ingredients = IngredientSerializer(many=True, read_only=True)
	tags = TagSerializer(many=True, read_only=True)