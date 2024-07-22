from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArtistViewSet, MoviesViewSet

router = DefaultRouter()
router.register(r'movies', MoviesViewSet, basename='movie')
router.register(r'artists', ArtistViewSet, basename='artist')

urlpatterns = [
    path('api/', include(router.urls))
]
