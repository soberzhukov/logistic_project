from rest_framework.serializers import ModelSerializer

from order.models import Order, SavedSearch
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


class GetSavedSearchSerializer(ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = SavedSearch
        fields = '__all__'
        depth = 1


class CreateDeleteSavedSearchSerializer(ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = '__all__'

    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs
