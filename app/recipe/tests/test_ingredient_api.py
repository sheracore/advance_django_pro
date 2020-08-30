from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):
	"""Test the publicly available ingredient API"""

	def setUp(self):
		self.client = APIClient()

	def test_login_required(self):
		"""Test that login is required for retrieveing tags"""
		res = self.client.get(INGREDIENT_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
	"""Test teh private ingredient API"""

	def setUp(self):
		self.client = APIClient()
		self.user = get_user_model().objects.create_user(
			'test@sheracore.com',
			'testpass'
			)

		self.client.force_authenticate(self.user)

	def test_retrieve_ingredient_list(self):
		"""Test retrieve a list of ingredient"""
		Ingredient.objects.create(user=self.user, name='kale')
		Ingredient.objects.create(user=self.user, name='Slat')

		res = self.client.get(INGREDIENT_URL)

		ingredient = Ingredient.objects.all().order_by('-name')
		serializer = IngredientSerializer(ingredient, many=True)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data, serializer.data)

	def test_ingredient_limited_to_user(self):
		"""Test that ingredient for the authenticated user are returned"""
		user2 = get_user_model().objects.create_user(
			'other@sheracore.com',
			'testpass'
			)
		Ingredient.objects.create(user=user2, name='Vinegare')
		ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')
		
		res = self.client.get(INGREDIENT_URL)
		
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		self.assertEqual(res.data[0]['name'], ingredient.name)

	def test_create_ingredient_successful(self):
		"""Test create a new ingredient"""
		payload = {'name': 'Cabbage'}
		self.client.post(INGREDIENT_URL, payload)
		
		exists = Ingredient.objects.filter(
			user=self.user,
			name=payload['name'],
			).exists()

		self.assertTrue(exists)

	def tset_create_ingredient_invalid(self):
		"""Test creating invalid ingredient fails"""
		payload = {'name': ''}
		res = self.client.post(INGREDIENT_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
