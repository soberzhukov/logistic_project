from django.db.models import Q
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from logisticproject.utils import BasicPagination
from .models import Contract
from .serializers import GetContractSerializer, UpdateContractSerializer


class CreateReadContractViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = GetContractSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetContractSerializer if self.action in ['list', 'retrieve'] else UpdateContractSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(executor=user) | Q(customer=user) |
                                    Q(order__author=user) | Q(offer__author=user))
