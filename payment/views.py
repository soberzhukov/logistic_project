from rest_framework import permissions
from rest_framework.generics import ListAPIView

from payment.models import PaymentMethod, Currency
from payment.serializers import PaymentMethodSerializer, CurrencySerializer


class PaymentMethodListAPIView(ListAPIView):
    queryset = PaymentMethod.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentMethodSerializer

class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CurrencySerializer