from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_description = """
The swagger documentation for GraphProject
"""

schema_view = get_schema_view(
    openapi.Info(
        title="APIs",
        default_version="v1",
        description=swagger_description,
        contact=openapi.Contact(email=""),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path("", include("movies.urls")),
    path("tools/", include("tools.urls"))
]
