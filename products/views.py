import requests
from django.core.cache import cache
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount, SocialApp
from products.serializers import RegistrationSerializer



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

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def telegram_user_view(request):
    return render(request, 'telegram_user_view.html')
bot1=f"hillel_telegram6_bot"
bot_id = f'7087030155:AAEjbzX8bgOZTeeRuBmbWGjQpgtLDAK1QUg'

def telegram_auth_view(request):
    try:
        telegram_app = SocialApp.objects.get(provider='telegram')
    except SocialApp.DoesNotExist:
        return redirect('/')

    #auth_url = f"https://api.telegram.org/bot7087030155:AAEjbzX8bgOZTeeRuBmbWGjQpgtLDAK1QUg/"
    auth_url = f"https://oauth.telegram.org/auth?bot_id={bot_id}&origin={bot1}&redirect_uri={'127.0.0.1:8000/'}"
    return redirect(auth_url)