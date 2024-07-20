from rest_framework.routers import DefaultRouter
from .views import MoviesViewSet, ArtistViewSet

router = DefaultRouter()
router.register(r'movies', MoviesViewSet, basename='movie')
router.register(r'artists', ArtistViewSet, basename='artist')

urlpatterns = router.urls