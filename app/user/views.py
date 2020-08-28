from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
	"""Create a new user in the system"""
	serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
	"""Create a new auth token for user"""
	serializer_class = AuthTokenSerializer
	# We can view this endpoing in the browser renderer is for browsable api
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
	"""Manage the authenticated user"""
	serializer_class = UserSerializer
	# Authentication could be cooki athentication or token ahtentiocation
	# Permission are the level of the access that the user have
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		"""Retrieve and return authenticated user"""
		return self.request.user