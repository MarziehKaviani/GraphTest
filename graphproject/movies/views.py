from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MovieSerializer, ArtistSerializer
import movies.variables as variables
from .validators import CountryValidator


class MoviesViewSet(viewsets.GenericViewSet,):
    """
    API endpoint that allows operations on Movies.

    This viewset provides `list`, `retrieve`, and `show_preview` actions for Movies objects.
    """
    queryset = MovieSerializer.get_queryset()
    serializer_class = MovieSerializer

    @action(detail=False, methods=[variables.POST])
    def create(self, request):
        """
        Create a new artist instance.

        This action allows creating a new artist.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        Response
            A response object containing the created artist details, HTTP status code.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=[variables.GET])
    def list(self, request):
        """
        Retrieve a list of all movies.

        This action returns a list of all movies available in the system.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        BaseResponse
            A response object containing the list of movies, HTTP status code, and business status code.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data=serializer.data,
            is_exception=False,
            http_status_code=status.HTTP_200_OK,
            )

    @action(detail=True, methods=[variables.GET])
    def retrieve(self, request, pk=None):
        """
        Retrieve the details of a specific movie.

        This action returns the details of a movie specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the movie to retrieve.

        Returns
        -------
        BaseResponse
            A response object containing the movie details, HTTP status code, and business status code.
        """
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=[variables.PUT, variables.PATCH])
    def update(self, request, pk=None):
        """
        Update a movie instance.

        This action allows updating a movie specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the movie to update.

        Returns
        -------
        BaseResponse
            A response object containing the updated movie details, HTTP status code, and business status code.
        """
        partial = request.method == 'PATCH'
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Movie not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=[variables.DELETE])
    def delete(self, request, pk=None):
        """
        Delete a movie instance.

        This action allows deleting a movie specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the movie to delete.

        Returns
        -------
        BaseResponse
            A response object indicating success or failure, HTTP status code, and business status code.
        """
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Movie not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.perform_destroy(instance)
        return Response(
            data={"detail": "Movie deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )



class ArtistViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows operations on Artists.

    This viewset provides `list`, `retrieve`, `create`, `update`, and `delete` actions for Artist objects.
    """
    queryset = ArtistSerializer().get_queryset()
    serializer_class = ArtistSerializer

    @action(detail=False, methods=[variables.GET])
    def list(self, request):
        """
        Retrieve a list of all artists.

        This action returns a list of all artists available in the system.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        Response
            A response object containing the list of artists, HTTP status code.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=[variables.GET])
    def retrieve(self, request, pk=None):
        """
        Retrieve the details of a specific artist.

        This action returns the details of an artist specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the artist to retrieve.

        Returns
        -------
        Response
            A response object containing the artist details, HTTP status code.
        """
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=[variables.POST])
    def create(self, request):
        """
        Create a new artist instance.

        This action allows creating a new artist.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        Response
            A response object containing the created artist details, HTTP status code.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=[variables.PUT, variables.PATCH])
    def update(self, request, pk=None):
        """
        Update an artist instance.

        This action allows updating an artist specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the artist to update.

        Returns
        -------
        Response
            A response object containing the updated artist details, HTTP status code.
        """
        partial = request.method == 'PATCH'
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=[variables.DELETE])
    def delete(self, request, pk=None):
        """
        Delete an artist instance.

        This action allows deleting an artist specified by its primary key.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the artist to delete.

        Returns
        -------
        Response
            A response object indicating success or failure, HTTP status code.
        """
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={"detail": "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(
            data={"detail": "Artist deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )