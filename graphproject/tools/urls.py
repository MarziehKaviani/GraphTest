from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EndpointCallCountViewSet

router = DefaultRouter()
router.register(r'endpoints', EndpointCallCountViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]