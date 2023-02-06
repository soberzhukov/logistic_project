from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .actions import CreateChat
from .models import ItemChat
from .serializers import ItemChatSerializer, MainChatSerializer


class CreateChatAPIView(CreateAPIView):
    """Создание чата"""
    serializer_class = ItemChatSerializer
    queryset = ItemChat.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        main_chat = CreateChat(self.request.user, serializer).create()
        main_chat_serializer = MainChatSerializer(main_chat, context={'request': request})
        return Response(main_chat_serializer.data, status=status.HTTP_201_CREATED)
