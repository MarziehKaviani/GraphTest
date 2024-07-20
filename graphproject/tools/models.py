from django.db import models


class EndpointCallCount(models.Model):
    endpoint = models.CharField(max_length=255, unique=True)
    call_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.endpoint}: {self.call_count}"