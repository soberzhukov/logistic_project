from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import GetOrderSerializer, UpdateOrderSerializer
from .filters import OrderFilter
from .permissions import IsOwner


class BasicPagination(PageNumberPagination):
    page_size = 10


class CRUDOrderViewSet(ModelViewSet):
    """CRUD without create"""
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetOrderSerializer if self.action in ['list', 'retrieve', 'create'] else UpdateOrderSerializer

    def create(self, request, *args, **kwargs):
        """POST request return list"""
        return super(CRUDOrderViewSet, self).list(request, *args, **kwargs)


class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class MyListOrdersAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Order.objects.filter(author=self.request.user)


class CounterOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count_views += 1
        instance.save()
        return Response(data={'message': 'ok'}, status=HTTP_200_OK)
