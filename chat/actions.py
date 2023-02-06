from typing import Type

from chat.models import MainChat, ItemChat
from chat.serializers import ItemChatSerializer, CreateChatMessageSerializer
from logisticproject.exceptions import BadeRequestException
from users.models import User


class CreateChat:
    def __init__(self, user: User, serializer: ItemChatSerializer):
        self._serializer = serializer
        self._user = user

    def create(self) -> MainChat:
        contract = self._serializer.validated_data.get('contract')

        customer = contract.customer

        main_chat, created = MainChat.objects.get_or_create(customer=customer, executor=self._user)

        if not created:
            items = main_chat.items_chat.filter(contract=contract)
            if items:
                serializer = ItemChatSerializer(items.last())
                return main_chat

        item_chat = self._serializer.save()
        main_chat.items_chat.add(item_chat)
        main_chat.save()
        return main_chat


class CreateChatMessage:
    def __init__(self, pk: str, user: User, data: dict, serializers_class: Type[CreateChatMessageSerializer]):
        self._pk = pk
        self._user = user
        self._data = data
        self._serializers_class = serializers_class

    def create(self) -> dict:
        self._data['author'] = self._user.id
        serializer = self._serializers_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        item_chat = self._get_item_chat()
        item_chat.messages.add(message)
        item_chat.save()

        return serializer.data

    def _get_item_chat(self) -> ItemChat:
        try:
            return ItemChat.objects.get(pk=self._pk)
        except ItemChat.DoesNotExist:
            raise BadeRequestException(
                message=f'Chat with this ID: {self._pk} was not found',
                code='chat_not_found')
