from django.db.models import Count, Q, Max
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from logisticproject.responses import CreatedResponse
from .actions import CreateChat, CreateChatMessage
from .models import ItemChat, MainChat, ChatMessage
from .serializers import ItemChatSerializer, MainChatSerializer, CreateChatMessageSerializer, GetMessages


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


class ListChatAPIView(ListAPIView):
    """Получение списка чатов"""
    serializer_class = MainChatSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = MainChat.objects.annotate(messages_count=Count('items_chat__messages')).filter(
            Q(executor=user) | Q(customer=user, messages_count__gt=0)).annotate(
            max_date=Max('items_chat__messages__date_created')).order_by('-max_date')
        return queryset

class RetrieveDeleteMainChatAPIView(RetrieveDestroyAPIView):
    """Удаление основного чата с заказчиком"""
    queryset = MainChat.objects.all()
    serializer_class = MainChatSerializer

    def delete(self, request, *args, **kwargs):
        main_chat = self.get_object()
        main_chat.items_chat.all().delete()
        return super().delete(request, *args, **kwargs)


class GetOrDeleteChatAPIView(RetrieveDestroyAPIView):
    """Получение или удаление чата с заказчиком"""
    serializer_class = ItemChatSerializer
    queryset = ItemChat.objects.all()

class GetMessagesAPIView(RetrieveDestroyAPIView):
    """Получение всех сообщений чата"""
    serializer_class = GetMessages
    queryset = ItemChat.objects.all()

class CreateChatMessageAPIView(CreateAPIView):
    """Создание сообщения чата"""
    serializer_class = CreateChatMessageSerializer
    queryset = ChatMessage.objects.all()

    def create(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.request.user
        response_data = CreateChatMessage(pk, user, self.request.data.copy(), self.serializer_class).create()
        return CreatedResponse(data=response_data)