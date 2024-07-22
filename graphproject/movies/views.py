from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import MovieSerializer, ArtistSerializer, EditActorsOfMovieSerializer
import movies.variables as variables
from .validators import CountryValidator, InputDataValidator
from .filters import MoviesFilter


class MoviesViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows operations on Movies.

    This viewset provides `list`, `retrieve`, and `show_preview` actions for Movies objects.
    """
    queryset = MovieSerializer.get_queryset()

    def get_serializer_class(self):
        if self.action in ['remove_actor', 'add_actor']:
            return EditActorsOfMovieSerializer
        else:
            return MovieSerializer
        
    def create(self, request, *args, **kwargs):
        """
        Create a new movie instance.

        This action allows creating a new movie.

        Parameters
        ----------
        request : Request
            The HTTP request object.

        Returns
        -------
        Response
            A response object containing the created movie details, HTTP status code.
        """

        # Check input data
        required_fields = [variables.NAME, variables.PRODUCTION_YEAR, variables.DIRECTOR, variables.ACTORS]
        if not InputDataValidator(request, required_fields=required_fields).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={variables.DETAILS: serializer.errors},
                exception=True,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Movie
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Apply filtering
        filterset = MoviesFilter(request.GET, queryset=self.get_queryset())
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Send filterd data to serializer
        queryset = filterset.qs
        serializer = self.get_serializer(queryset, many=True)
        
        # Return movies list
        return Response(
            data=serializer.data,
            exception=False,
            status=status.HTTP_200_OK,
            )

    def retrieve(self, request, pk=None, *args, **kwargs):
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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: variables.MOVIE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        
        # Retrieve
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None, *args, **kwargs):
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
        # Check input data
        fields = [variables.NAME, variables.PRODUCTION_YEAR, variables.DIRECTOR, variables.ACTORS]

        partial=request.method==variables.PATCH
        if partial:
            if not InputDataValidator(request=request, optional_fields=fields).validate():
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)
        else:
            if not InputDataValidator(request=request, required_fields=fields).validate():
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: variables.MOVIE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                data={variables.DETAILS: serializer.errors},
                exception=True,
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Update
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None, *args, **kwargs):

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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Delete movie
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: variables.MOVIE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(
            data={variables.DETAILS: "Movie deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
    
    @action(detail=True, methods=[variables.POST])
    def add_actor(self, request, pk=None):
        """
        Add an actor to a specific movie's actors list.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the movie.

        Returns
        -------
        Response
            A response object indicating success or failure, HTTP status code.
        """
        # Check input data
        required_fields = [variables.ACTOR_ID]
        validator = InputDataValidator(request, required_fields=required_fields)
        if not validator.validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=variables.INVALID_INPUT_DATA)

        # Add actor
        actor_id = request.data.get(variables.ACTOR_ID)
        movie = self.get_queryset().filter(pk=pk).first()
        if not movie:
            return Response(
                data={variables.DETAILS: variables.MOVIE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        actor = ArtistSerializer().get_queryset().filter(pk=actor_id).first()
        if not actor:
            return Response(
                data={variables.DETAILS: variables.ARTIST_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.actors.add(actor)
        movie.save()
        return Response(
            data={variables.DETAILS: "Actor added successfully."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=[variables.POST])
    def remove_actor(self, request, pk=None):
        """
        Remove an actor from a specific movie's actors list.

        Parameters
        ----------
        request : Request
            The HTTP request object.
        pk : int, optional
            The primary key of the movie.

        Returns
        -------
        Response
            A response object indicating success or failure, HTTP status code.
        """
        # Check input data
        required_fields = [variables.ACTOR_ID]
        validator = InputDataValidator(request, required_fields=required_fields)
        if not validator.validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=variables.INVALID_INPUT_DATA)

        # Remove actor
        actor_id = request.data.get(variables.ACTOR_ID)
        movie = self.get_queryset().filter(pk=pk).first()
        if not movie:
            return Response(
                data={variables.DETAILS: variables.MOVIE_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        actor = ArtistSerializer().get_queryset().filter(pk=actor_id).first()
        if not actor:
            return Response(
                data={variables.DETAILS: variables.ARTIST_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not movie.actors.filter(pk=actor.pk).exists():
            return Response(
                data={variables.DETAILS: "The selected actor is not one of the movie's actors"},
                status=status.HTTP_404_NOT_FOUND
            )

        movie.actors.remove(actor)
        movie.save()
        return Response(
            data={variables.DETAILS: "Actor removed successfully."},
            status=status.HTTP_200_OK
        )


class ArtistViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows operations on Artists.

    This viewset provides `list`, `retrieve`, `create`, `update`, and `delete` actions for Artist objects.
    """
    queryset = ArtistSerializer().get_queryset()
    serializer_class = ArtistSerializer

    def list(self, request, *args, **kwargs):
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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        
        # Return Artists List
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        
        # Retrieve artist
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
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
        # Check input data
        required_fields = [variables.FULL_NAME, variables.COUNTRY, variables.DOB]
        
        if variables.COUNTRY in request.data:
            if not CountryValidator().is_valid(request.data[variables.COUNTRY]):
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)
            
        if not InputDataValidator(request=request, required_fields=required_fields).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)
       
        # Send data to serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return Response(
                data={variables.DETAILS: serializer.errors},
                exception=True,
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Create
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None, *args, **kwargs):
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
        # Check input data
        fields = [variables.FULL_NAME, variables.COUNTRY, variables.DOB]
        if variables.COUNTRY in request.data:
            if not CountryValidator().is_valid(request.data[variables.COUNTRY]):
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)
            
        partial=request.method==variables.PATCH
        if partial:
            if not InputDataValidator(request=request, optional_fields=fields).validate():
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)
        else:
            if not InputDataValidator(request=request, required_fields=fields).validate():
                return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Send data to serializer
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                data={variables.DETAILS: serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
                exception=True
            )
        
        # Update
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None, *args, **kwargs):
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
        # Check input data
        if not InputDataValidator(request).validate():
            return Response(status=status.HTTP_400_BAD_REQUEST, exception=True, data=variables.INVALID_INPUT_DATA)

        # Delete Artist
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response(
                data={variables.DETAILS: "Artist not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(
            data={variables.DETAILS: "Artist deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )