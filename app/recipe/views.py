from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin,
							mixins.CreateModelMixin):
	"""Base viewset for user owned recipe attrubutes"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		"""Return objects for the current authenticated user"""
		# This self.request.user filters the user that currently authenticated
		return self.queryset.filter(user=self.request.user).order_by('-name')

	def perform_create(self, serializer):
		"""Create a new object"""
		serializer.save(user=self.request.user)



# class TagViewSet(viewsets.GenericViewSet, 
# 				 mixins.ListModelMixin,
# 				 mixins.CreateModelMixin):
class TagViewSet(BaseRecipeAttrViewSet):
	"""Manage tags in the database"""
	queryset = Tag.objects.all()
	serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
	"""Manage ingredient in the database"""
	queryset = Ingredient.objects.all()
	serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
	"""Manage recipes in the database"""
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		"""Retrieve the recipes for the authenticated user"""
		return  self.queryset.filter(user=self.request.user)
