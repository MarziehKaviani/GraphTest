from django.db.models import QuerySet
from rest_framework import serializers

from .models import Artists, Movies


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movies model.

    Attributes:
    ----------
    * `Meta`: ``class``
        Configuration class for the serializer.

        - `model`: ``Movie``
            The Movie model.
        - `fields`: ``str`` or ``list``
            The fields to include in the serialized representation.
    """

    def get_queryset() -> QuerySet:
        return Movies.objects.all()

    def get_movie(pk) -> Movies:
        return Movies.objects.get(pk=pk)

    class Meta:
        model = Movies
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    """
    Serializer for Artists model.

    Attributes:
    ----------
    * `Meta`: ``class``
        Configuration class for the serializer.

        - `model`: ``Artists``
            The Artists model.
        - `fields`: ``str`` or ``list``
            The fields to include in the serialized representation.
    """

    def get_queryset(self) -> QuerySet:
        return Artists.objects.all()

    class Meta:
        model = Artists
        fields = '__all__'


class EditActorsOfMovieSerializer(serializers.Serializer):
    actor_id = serializers.CharField(max_length=5)
