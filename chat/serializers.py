from rest_framework import serializers

from common.serializers import FileSerializer
from users.serializers import UserInfoSerializer
from .models import ItemChat, ChatMessage, MainChat


class ChatMessageSerializer(serializers.ModelSerializer):
    chat_files = FileSerializer(many=True, read_only=True)
    """Сериализатор сообщений чата"""

    class Meta:
        model = ChatMessage
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class ItemChatSerializer(serializers.ModelSerializer):
    """Сериализатор предмета чата, используется для создания чата"""
    messages = ChatMessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField('get_last_message')

    class Meta:
        model = ItemChat
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}}

    def get_last_message(self, obj):
        return obj.messages.last()


class MainChatSerializer(serializers.ModelSerializer):
    """Сериализатор получения списка чатов"""
    items_chat = ItemChatSerializer(many=True)
    executor = UserInfoSerializer(read_only=True)
    customer = UserInfoSerializer(read_only=True)
    request_user = serializers.SerializerMethodField('get_request_user')

    class Meta:
        model = MainChat
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}}

    def get_request_user(self, obj):
        user = self.context['request'].user
        request = self.context.get('request', None)
        return UserInfoSerializer(instance=user,
                                  context={'request': request}).data


class CreateChatMessageSerializer(serializers.ModelSerializer):
    """Сериализатор создания сообщения чата"""
    class Meta:
        model = ChatMessage
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True},
                        "text": {"required": False}}


    def validate(self, attrs):
        if not attrs.get('text') and not attrs.get('chat_files'):
            raise serializers.ValidationError(
                detail='You must forward at least one of these fields text or chat_files')

        return super().validate(attrs)