from rest_framework.serializers import ModelSerializer

from order.models import Order
from users.serializers import GetUserSerializer


class GetOrderSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

