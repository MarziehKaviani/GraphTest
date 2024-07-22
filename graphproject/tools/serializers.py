from rest_framework import serializers
from .models import EndpointCallCount


class EndpointCallCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointCallCount
        fields = ['endpoint', 'call_count', 'method']