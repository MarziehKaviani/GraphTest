from django.utils.deprecation import MiddlewareMixin
from .models import EndpointCallCount

class EndpointCallCountMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        endpoint = request.path
        if response.status_code == 200:  # You can customize this condition as needed
            obj, created = EndpointCallCount.objects.get_or_create(endpoint=endpoint)
            if not created:
                obj.call_count += 1
                obj.save()
        return response