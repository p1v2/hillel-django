from django.contrib.auth.models import User
from rest_framework import authentication


class MyCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        get_params = request.query_params

        user = User.objects.get(username="vitalii")

        if get_params.get("haslo") == "SlavaUkraini":
            return user, None
        else:
            return None, None
