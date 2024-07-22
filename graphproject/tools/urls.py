from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EndpointCallCountViewSet, PostgresqlExtensionAPIView

router = DefaultRouter()
router.register('endpoints', EndpointCallCountViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/postgresql_extentions', PostgresqlExtensionAPIView.as_view())
]
