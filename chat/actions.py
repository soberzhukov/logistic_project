from chat.serializers import ItemChatSerializer

from chat.models import MainChat
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
                # return serializer.data
        item_chat = self._serializer.save()
        main_chat.items_chat.add(item_chat)
        main_chat.save()
        return main_chat  # self._serializer.data



