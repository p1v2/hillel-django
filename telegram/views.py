from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from telegram.client import send_message


class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class MessageSerializer(serializers.Serializer):
    chat = ChatSerializer()


class TelegramSerializer(serializers.Serializer):
     message = MessageSerializer()


# Create your views here.
@swagger_auto_schema(methods=['post'], request_body=TelegramSerializer, responses={200: "OK"})
@api_view(["POST"])
@permission_classes([])
def accept_telegram_message(request):
    chat_id = request.data["message"]["chat"]["id"]
    text = "How are you?"

    send_message(text, chat_id)

    return Response({"status": "ok"})
