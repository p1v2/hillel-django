from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class GloryToUkraineAuthentication(BaseAuthentication):
    def authenticate(self, request):
        query_params = request.GET

        if query_params.get("haslo") == "SlavaUkraini":
            return User.objects.get(username="vitaliipavliuk"), None


class SecretHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        secret_header = request.META.get("HTTP_SECRET_HEADER")

        if secret_header is None:
            return None, None

        if secret_header.startswith("Some super secret"):
            username = secret_header.split(' ')[-1]
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist as e:
                print(e)
                return None, None
            else:
                return user, None
