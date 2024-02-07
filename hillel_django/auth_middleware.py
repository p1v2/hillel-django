from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            messages.error(request, 'Authentication failed.')
            return redirect('login')