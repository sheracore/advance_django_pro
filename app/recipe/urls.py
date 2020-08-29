from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# DefaultRouter is django feature that automaticly generate urls for our viewset
# And uses for make all type of urls
# Like */api/recipe/tags/ || */api/recipe/tags/1/
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]