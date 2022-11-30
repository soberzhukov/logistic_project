from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from logisticproject.utils import BasicPagination
from offer.models import Offer
from offer.serializers import GetOfferSerializer, UpdateOfferSerializer
from users.permissions import IsAuthor
from .filters import OfferFilter


class CRUDOfferViewSet(ModelViewSet):
    """CRUD without create"""
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = (IsAuthor,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter
    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetOfferSerializer if self.action in ['list', 'retrieve', 'create'] else UpdateOfferSerializer

    def create(self, request, *args, **kwargs):
        """Пост запрос возвращает список"""
        return super(CRUDOfferViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset.annotate(count_cs=Count('contracts_offer')).filter(max_contracts__gt=F('count_cs'))
        if self.request.method not in ['POST', 'GET']:
            return self.queryset.filter(author=self.request.user)
        if self.request.user.is_authenticated and self.action == 'retrieve':
            queryset = queryset | self.queryset.filter(author=self.request.user)
        return queryset.distinct()


class CreateOfferAPIView(CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = UpdateOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MyListOffersAPIView(ListAPIView):
    """Мой лист"""
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user)


class CounterOfferAPIView(CreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count_views += 1
        instance.save()
        return Response(data={'message': 'ok'}, status=HTTP_200_OK)
