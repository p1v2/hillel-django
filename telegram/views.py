from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from telegram.client import send_message


# Create your views here.
@api_view(["POST"])
@permission_classes([])
def accept_telegram_message(request):
    chat_id = request.data["message"]["chat"]["id"]
    text = "How are you?"

    send_message(text, chat_id)

    return Response({"status": "ok"})
