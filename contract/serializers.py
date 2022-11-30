from rest_framework import serializers

from offer.serializers import GetOfferSerializer
from order.serializers import GetOrderSerializer
from users.serializers import GetUserSerializer
from .models import Contract


class GetContractSerializer(serializers.ModelSerializer):
    customer = GetUserSerializer()
    executor = GetUserSerializer()
    order = GetOrderSerializer()
    offer = GetOfferSerializer()

    class Meta:
        model = Contract
        fields = '__all__'
        depth = 1


class UpdateContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

    def validate(self, attrs):
        if (not attrs.get('offer') and not attrs.get('order')) or (attrs.get('offer') and attrs.get('order')):
            raise serializers.ValidationError('offer or order - one of fields is required')
        user = self.context['request'].user
        if attrs.get('offer'):
            attrs['customer'] = user
        if attrs.get('order'):
            attrs['executor'] = user
        return attrs
