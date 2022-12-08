from rest_framework import permissions
from rest_framework.generics import ListAPIView

from payment.models import PaymentMethod
from payment.serializers import PaymentMethodSerializer


class PaymentMethodListAPIView(ListAPIView):
    queryset = PaymentMethod.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentMethodSerializer
