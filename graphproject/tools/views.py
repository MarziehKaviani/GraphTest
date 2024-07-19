from rest_framework.response import Response
from rest_framework.views import APIView


class PostgresqlExtensionAPIView(APIView):
    """
    This is The APIView to return the installed extensions of the database.
    """
    def get(self, request, *args, **kwargs):
        #! TODO: This part should be done.
        return Response({"message": "Extensions should be provided!"})
