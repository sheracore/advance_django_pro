from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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
    
    # override serializer
	def get_serializer_class(self):
		"""Return appropriate serializer class"""
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer
		elif self.action == 'upload_image':
			return serializers.RecipeImageSerializer

		return self.serializer_class

	def perform_create(self, serializer):
		"""Create a new recipe"""
		serializer.save(user=self.request.user)
    
    # Derail meanse POST url contain id ---> recipe/id/upload-image
	@action(methods=['POST'], detail=True, url_path='upload-image')
	def upload_image(self, request, pk=None):
		print("**************")
		"""Upload an image to a recipe"""
		# get_object is based on id
		recipe = self.get_object()
		serializer = self.get_serializer(
			recipe,
			data=request.data
			)

		if serializer.is_valid():
			serializer.save()
			return Response(
					serializer.data,
					status=status.HTTP_200_OK
				)

		return Response(
			serializer.errors,
			status=status.HTTP_400_BAD_REQUEST
			)