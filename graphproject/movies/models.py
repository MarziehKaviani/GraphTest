from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

import movies.variables as variables
from .validators import YearValidator


class Artists(models.Model):
    full_name = models.CharField(
        max_length=255,
        verbose_name=_(variables.NAME_VERBOSE),
    )
    country = models.CharField(
        max_length=2,  # IsoAlpha2 stores in db
        verbose_name=_(variables.COUNTRY_VERBOSE)
    )


class Movies(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_(variables.NAME_VERBOSE),
    )
    production_year = models.IntegerField(
        verbose_name=_(variables.PRODUCTION_YEAR_VERBOSE),
        validators=[MinValueValidator(1984), YearValidator.max_year_validator]
    )
    director = models.OneToOneField(
        Artists,
        on_delete=models.SET_NULL,
        null=True,
        related_name=variables.MOVIES_DIRECTOR_RELATED_NAME,
        verbose_name=_(variables.DIRECTOR_VERBOSE)
    )
    actors = models.ManyToManyField(
        Artists,
        related_name=variables.MOVIES_ACTORS_RELATED_NAME,
        verbose_name=_(variables.ACTORS_VERBOSE)
    )

