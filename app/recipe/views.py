from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    
    # Overwrite get queryset
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # This self.request.user filters authenticated users
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    # It is an function that allows us to create process
    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)