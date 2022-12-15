from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from common.views import CRUDObjectViewSet, ElectedViewSet, CounterObjectAPIView
from logisticproject.utils import BasicPagination
from order.models import Order, ElectedOrder
from order.serializers import GetOrderSerializer, UpdateOrderSerializer, GetElectedOrderSerializer, \
    UpdateElectedOrderSerializer
from .filters import OrderFilter


class CRUDOrderViewSet(CRUDObjectViewSet):
    """CRUD without create"""
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_serializer_class(self):
        return GetOrderSerializer if self.action in self.read_action_list else UpdateOrderSerializer

    def get_queryset(self, *args, **kwargs):
        super().get_queryset(contracts_field='contracts_order')


class CreateOrderAPIView(CreateAPIView):
    """Создание заказа"""
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MyListOrdersAPIView(ListAPIView):
    """Список моих заказов"""
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Order.objects.filter(author=self.request.user)


class CounterOrderAPIView(CounterObjectAPIView):
    """Счетчик просмотров"""
    queryset = Order.objects.all()


class ElectedOrderViewSet(ElectedViewSet):
    queryset = ElectedOrder.objects.all()
    serializer_class = GetElectedOrderSerializer

    def get_serializer_class(self):
        return GetElectedOrderSerializer if self.action in self.read_action_list else UpdateElectedOrderSerializer
