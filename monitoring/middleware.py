# myapp/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import add_never_cache_headers

class DisableCachingOnAuthPages(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            add_never_cache_headers(response)
        return response
