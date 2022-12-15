from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from common.views import CRUDObjectViewSet, CounterObjectAPIView, ElectedViewSet
from logisticproject.utils import BasicPagination
from offer.models import Offer, ElectedOffer
from offer.serializers import GetOfferSerializer, UpdateOfferSerializer, GetElectedOfferSerializer, \
    UpdateElectedOfferSerializer
from .filters import OfferFilter


class CRUDOfferViewSet(CRUDObjectViewSet):
    """CRUD without create"""
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter

    def get_serializer_class(self):
        return GetOfferSerializer if self.action in self.read_action_list else UpdateOfferSerializer

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(contracts_field='contracts_offer')


class CreateOfferAPIView(CreateAPIView):
    """Создание предложения"""
    queryset = Offer.objects.all()
    serializer_class = UpdateOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MyListOffersAPIView(ListAPIView):
    """Список моих предложений"""
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user)


class CounterOfferAPIView(CounterObjectAPIView):
    """Счетчик просмотров"""
    queryset = Offer.objects.all()


class ElectedOfferViewSet(ElectedViewSet):
    queryset = ElectedOffer.objects.all()
    serializer_class = GetElectedOfferSerializer

    def get_serializer_class(self):
        return GetElectedOfferSerializer if self.action in self.read_action_list else UpdateElectedOfferSerializer
