from rest_framework.response import Response
from rest_framework import viewsets, views
from django.db import connection

from .models import EndpointCallCount
from .serializers import EndpointCallCountSerializer


class PostgresqlExtensionAPIView(views.APIView):
    """
    API endpoint to retrieve installed PostgreSQL extensions.

    This API view provides information about the installed extensions in the PostgreSQL
    database by querying the `pg_extension` system catalog table.

    Methods
    -------
    get(request, *args, **kwargs)
        Handles GET requests and returns a list of installed PostgreSQL extensions with their versions.
    
    Returns
    -------
    Response
        A Django Rest Framework Response object containing the list of installed extensions and their versions.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieve installed PostgreSQL extensions.

        Executes a SQL query to fetch the names and versions of all installed PostgreSQL extensions.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request object.

        Returns
        -------
        Response
            A Response object with a JSON payload containing a list of dictionaries, each representing an
            installed extension with its name and version.
        """
        query = """
            SELECT 
                extname AS extension_name,
                extversion AS version
            FROM 
                pg_extension;
        """
        
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        
        # Process the result
        extensions = []
        for row in rows:
            extension = {
                'extension_name': row[0],
                'version': row[1]
            }
            extensions.append(extension)
        
        return Response({'extensions': extensions})
    

class EndpointCallCountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for retrieving endpoint call count records.

    Provides read-only operations to list and retrieve records of endpoint call counts.

    Attributes
    ----------
    queryset : django.db.models.query.QuerySet
        The queryset used to retrieve EndpointCallCount objects.
    serializer_class : serializers.ModelSerializer
        The serializer class used to serialize and deserialize EndpointCallCount objects.
    """
    queryset = EndpointCallCount.objects.all()
    serializer_class = EndpointCallCountSerializer