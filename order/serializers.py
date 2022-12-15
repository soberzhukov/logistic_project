from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from order.models import Order, ElectedOrder
from users.serializers import GetUserSerializer


class GetOrderSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class UpdateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs


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
