from rest_framework import serializers

from payment.models import PaymentMethod, Currency


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'