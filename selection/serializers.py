from rest_framework import serializers

from offer.serializers import GetOfferSerializer
from order.serializers import GetOrderSerializer
from selection.models import SelectionOrder, SelectionOffer


class SelectionOrderSerializer(serializers.ModelSerializer):
    orders = GetOrderSerializer(many=True)

    class Meta:
        model = SelectionOrder
        fields = '__all__'
        depth = 1


class SelectionOfferSerializer(serializers.ModelSerializer):
    offers = GetOfferSerializer(many=True)

    class Meta:
        model = SelectionOffer
        fields = '__all__'
        depth = 1