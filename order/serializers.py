from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from common.serializers import GetObjectSerializer, UpdateObjectSerializer
from order.models import Order, ElectedOrder
from users.serializers import GetUserSerializer


class GetOrderSerializer(GetObjectSerializer):
    class Meta(GetObjectSerializer.Meta):
        model = Order


class UpdateOrderSerializer(UpdateObjectSerializer):
    class Meta(UpdateObjectSerializer.Meta):
        model = Order


class GetElectedOrderSerializer(ModelSerializer):
    user = GetUserSerializer()

    class Meta:
        model = ElectedOrder
        fields = '__all__'
        depth = 1


class UpdateElectedOrderSerializer(ModelSerializer):
    class Meta:
        model = ElectedOrder
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        if ElectedOrder.objects.filter(user=user, order=attrs.get('order')).exists():
            raise serializers.ValidationError([f"{attrs['order'].id} - already exists."])
        return attrs
