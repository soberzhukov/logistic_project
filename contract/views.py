from django.db.models import Q
from rest_framework import permissions, mixins
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.viewsets import GenericViewSet

from logisticproject.utils import BasicPagination
from .models import Contract
from .serializers import GetContractSerializer, CreateContractSerializer, StatusContractSerializer


class CreateReadContractViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = GetContractSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetContractSerializer if self.action in ['list', 'retrieve'] else CreateContractSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(executor=user) | Q(customer=user) |
                                    Q(order__author=user) | Q(offer__author=user))


class ChangeStatusAPIView(mixins.UpdateModelMixin,
                          GenericAPIView):
    """Изменение статуса контракта, доступ у владельца order/offer"""
    queryset = Contract.objects.all()
    serializer_class = StatusContractSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(self.queryset.filter(Q(order__author=user) | Q(offer__author=user)), **self.kwargs)
        return obj
