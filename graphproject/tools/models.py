from django.db import models


class EndpointCallCount(models.Model):
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    call_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('endpoint', 'method')

    def __str__(self):
        return f"{self.endpoint}: {self.call_count}"
