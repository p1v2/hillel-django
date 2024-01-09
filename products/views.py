from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render
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


def error_auth(request):
    # Ваш код обработки входа в систему

    # Если вход в систему не удался, добавьте сообщение об ошибке
    if not request.user.is_authenticated:
        messages.error(request, "Failed to log in. Please check your credentials.")

    # Далее ваш код представления
    return render(request, 'index.html')