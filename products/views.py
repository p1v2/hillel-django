import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response

@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    registration_data = request.data

    serializer = RegistrationSerializer(data=registration_data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def github_user_view(request):
    username = request.query_params.get("username")
    print(username)

    cached_data = cache.get(f"github_user_{username}")

    if cached_data:
        print("From cache")
        return Response(cached_data)

    github_response = requests.get(
        f"https://api.github.com/users/{username}",
    )

    cache.set(f"github_user_{username}", github_response.json(), timeout=3600)
    print("From github")

    return Response(github_response.json())