from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

""" Notic that:
    every single test than runs it refreshes the database
    So the user that were created in test_create_valid_user_success
    are not going to be accessible in test_password_too_short
"""

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Unauthentication user test
# private test(password or modify user) expect to be authenticated
class PublicUserApiTests(TestCase):
    """ Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        """payload is the object that you pass to the api when you make request"""
        payload = {
            'email' : 'test@sheracore.com',
            'password' : 'testpass',
            'name' : 'Test name' 
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Test creating a user realy exists fails"""
        payload = {'email': 'test@sheracore.com', 'password': 'testpass'}
        create_user(**payload)
        
        # This is bad request bacause it's already exist(created last line above)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 chatacters"""
        
        payload = {'email': 'test@sheracore.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a toke is created for the user"""
        payload = {'email': 'tst@sheracore.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@sheracore.com', password='testpass')
        payload = {'email': 'test@sheracore.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_craete_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@sheracore.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)