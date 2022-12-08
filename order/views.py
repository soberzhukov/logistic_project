from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from logisticproject.utils import BasicPagination
from order.models import Order, SavedSearch, ElectedOrder
from order.serializers import GetOrderSerializer, UpdateOrderSerializer, GetSavedSearchSerializer, \
    CreateDeleteSavedSearchSerializer, GetElectedOrderSerializer, UpdateElectedOrderSerializer
from users.permissions import IsAuthor
from .filters import OrderFilter


class CRUDOrderViewSet(ModelViewSet):
    """CRUD without create"""
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (IsAuthor,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetOrderSerializer if self.action in ['list', 'retrieve', 'create'] else UpdateOrderSerializer

    def create(self, request, *args, **kwargs):
        """Пост запрос возвращает список"""
        return super(CRUDOrderViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.annotate(count_cs=Count('contracts_order')).filter(max_contracts__gt=F('count_cs')).exclude(status='draft')
        if self.request.method not in ['POST', 'GET']:
            # пользователь может обновлять и удалять только свои ордера
            return self.queryset.filter(author=self.request.user)
        if self.request.user.is_authenticated and self.action == 'retrieve':
            # авторизованный пользователь может получить свой ордер, даже если количество контракторов заполнено
            queryset = queryset | self.queryset.filter(author=self.request.user)
        elif self.request.user.is_authenticated:
            # исключаю из списка ордеры автора
            queryset = queryset.exclude(author=self.request.user)
        return queryset.distinct()


class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MyListOrdersAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

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


class SearchViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = SavedSearch.objects.all()
    serializer_class = GetSavedSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetSavedSearchSerializer if self.action in ['list', 'retrieve'] else CreateDeleteSavedSearchSerializer

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class ElectedOrderViewSet(ModelViewSet):
    queryset = ElectedOrder.objects.all()
    serializer_class = GetElectedOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetElectedOrderSerializer if self.action in ['list', 'retrieve'] else UpdateElectedOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
