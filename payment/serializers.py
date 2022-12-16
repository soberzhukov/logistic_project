from rest_framework import serializers

from payment.models import PaymentMethod, Currency, Budget


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    class Meta:
        model = Budget
        fields = '__all__'