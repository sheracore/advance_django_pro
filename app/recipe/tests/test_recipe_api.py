from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

# /api/recipe/recipes
# /api/recipe/recipes/1/
RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
	"""Return recipe detail URL"""
	return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='Main course'):
	"""Create and return a sample tag"""
	return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Cinnamon'):
	"""Create and return a sample ingredient"""
	return Ingredient.objects.create(user=user, name=name)

def sample_recipe(user, **params):
	"""Create and return a sample recipe"""
	defualts = {
		'title' : 'Sample recipe',
		'time_minutes' : 10,
		'price': 5.00
	}
	defualts.update(params)

	return Recipe.objects.create(user=user, **defualts)


class PublicRecipeApiTests(TestCase):
	"""Test unauthenticated recipe API access"""
	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(RECIPE_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PriveteRecipeApiTest(TestCase):
	"""Test aunauthenticated recipe API access"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'test@sheracore.com',
			'testpass'
			)
		self.client.force_authenticate(self.user)

	def test_retrieve_recipe(self):
		"""Test retrieving a list of recipe"""
		sample_recipe(user=self.user)
		sample_recipe(user=self.user)

		res = self.client.get(RECIPE_URL)

		recipes = Recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_recipe_limited_to_user(self):
		"""Test retriving recipe for user"""
		user2 = get_user_model().objects.create_user(
			'other@sheracore.com',
			'passtest'
			)
		sample_recipe(user=user2)
		sample_recipe(user=self.user)

		res = self.client.get(RECIPE_URL)

		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data, serializer.data)

	def test_view_recipe_detail(self):
		"""Test viewing a recipe detail"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		recipe.ingredients.add(sample_ingredient(user=self.user))

		url = detail_url(recipe.id)
		res = self.client.get(url)

		serializer = RecipeDetailSerializer(recipe)
		self.assertEqual(res.data, serializer.data)
