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


class CreateContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ['file', 'comment']

    def validate(self, attrs):
        if (not attrs.get('offer') and not attrs.get('order')) or (attrs.get('offer') and attrs.get('order')):
            raise serializers.ValidationError('offer or order - one of fields is required')
        user = self.context['request'].user
        if attrs.get('offer'):
            attrs['customer'] = user
        if attrs.get('order'):
            attrs['executor'] = user
        return attrs

    def validate_order(self, obj):
        if obj.max_contracts <= obj.contracts_order.count():
            raise serializers.ValidationError('max_contracts')
        return obj

    def validate_offer(self, obj):
        if obj.max_contracts <= obj.contracts_offer.count():
            raise serializers.ValidationError('max_contracts')
        return obj


class StatusContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['status', 'file', 'comment']
