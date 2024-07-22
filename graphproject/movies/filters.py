import django_filters

from .models import Movies


class MoviesFilter(django_filters.FilterSet):
    director = django_filters.CharFilter(
        field_name='director__full_name', lookup_expr='icontains')
    actors = django_filters.CharFilter(
        field_name='actors__full_name', method='filter_actors')

    class Meta:
        model = Movies
        fields = ['director', 'actors']

    def filter_actors(self, queryset, name, value):
        actor_names = value.split(',')
        for actor_name in actor_names:
            queryset = queryset.filter(actors__full_name__icontains=actor_name)
        return queryset
