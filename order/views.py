from rest_framework import permissions, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from order.models import Order
from order.serializers import GetOrderSerializer, UpdateOrderSerializer
from .permissions import IsOwner


class BasicPagination(PageNumberPagination):
    page_size = 10


class CRUDOrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetOrderSerializer if self.action in ['list', 'retrieve'] else UpdateOrderSerializer


class MyListOrdersViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Order.objects.filter(author=self.request.user)
