from django.utils.deprecation import MiddlewareMixin
from django.db.models import F
from .models import EndpointCallCount

class EndpointCallCountMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        path = self.normalize_path(request.path)
        method = request.method
        
        if path:
            endpoint_call, created = EndpointCallCount.objects.get_or_create(endpoint=path, method=method)
            endpoint_call.call_count = F('call_count') + 1
            endpoint_call.save()
        
        return response

    def normalize_path(self, path):
        segments = path.strip('/').split('/')
        if segments and segments[-1].isdigit():
            segments.pop()
        normalized_path = '/' + '/'.join(segments) + '/'
        return normalized_path

