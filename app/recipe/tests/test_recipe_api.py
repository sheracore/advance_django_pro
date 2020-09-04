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

	def test_create_basic_recipe(self):
		"""Test creating recipe"""
		payload = {
			'title': 'Chocolate cheesecake',
			'time_minutes': 30,
			'price': 5.00 
		}
		res = self.client.post(RECIPE_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		for key in payload.keys():
			# getattr(recipe, key) == recipe.title, recipe.time_minutes and ..
			self.assertEqual(payload[key], getattr(recipe, key))

	def test_create_recipe_with_tags(self):
		"""Test creating a recipe with tags"""
		tag1 = sample_tag(user=self.user, name='Vegan')
		tag2 = sample_tag(user=self.user, name='Dessert')
		payload = {
			'title': 'Avocado lime cheesecake',
			'tags': [tag1.id, tag2.id],
			'time_minutes': 60,
			'price': 20.00
		}
		res = self.client.post(RECIPE_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		tags = recipe.tags.all()
		self.assertEqual(tags.count(), 2)
		self.assertIn(tag1, tags)
		self.assertIn(tag2, tags)

	def test_create_recipe_with_ingredient(self):
		"""Test creating recipe with ingredient"""
		ingredient1 = sample_ingredient(user=self.user, name='Prawns')
		ingredient2 = sample_ingredient(user=self.user, name='Ginger')
		payload = {
			'title': 'Thai prawn red curry',
			'ingredients': [ingredient1.id, ingredient2.id],
			'time_minutes': 20,
			'price': 7.00
		}
		res = self.client.post(RECIPE_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		recipe = Recipe.objects.get(id=res.data['id'])
		ingredients = recipe.ingredients.all()
		self.assertEqual(ingredients.count(), 2)
		self.assertIn(ingredient1, ingredients)
		self.assertIn(ingredient2, ingredients)

	def test_partial_update_recipe(self):
		"""Test updating a recipe with patch"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		new_tag = sample_tag(user=self.user, name='Curry')

		payload = {'title': 'chicken tikka', 'tags': [new_tag.id]}
		url = detail_url(recipe.id)
		self.client.patch(url, payload)
        
        # If vlues changed from the database it needs to refresh the DB
		recipe.refresh_from_db()
		self.assertEqual(recipe.title, payload['title'])
		tags = recipe.tags.all()
		# tags.count() = len(tags)
		self.assertEqual(len(tags), 1)
		self.assertIn(new_tag, tags)

	def test_full_update_recipe(self):
		"""Test updating a recipe with put"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		payload = {
		'title': 'spaghetti carconara',
		'time_minutes': 25,
		'price': 5.00
		}
		url = detail_url(recipe.id)
		self.client.put(url, payload)

		recipe.refresh_from_db()
		self.assertEqual(recipe.title, payload['title'])
		self.assertEqual(recipe.time_minutes, payload['time_minutes'])
		self.assertEqual(recipe.price, payload['price'])
		tags = recipe.tags.all()
		self.assertEqual(len(tags), 0)