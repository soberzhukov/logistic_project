from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from offer.models import Offer
from offer.serializers import GetOfferSerializer, UpdateOfferSerializer
from .permissions import IsOwner


class BasicPagination(PageNumberPagination):
    page_size = 10


class CRUDOfferViewSet(ModelViewSet):
    """CRUD without create"""
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    pagination_class = BasicPagination

    def get_serializer_class(self):
        return GetOfferSerializer if self.action in ['list', 'retrieve', 'create'] else UpdateOfferSerializer

    def create(self, request, *args, **kwargs):
        """POST request return list"""
        return super(CRUDOfferViewSet, self).list(request, *args, **kwargs)


class CreateOfferAPIView(CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = UpdateOfferSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class MyListOffersAPIView(ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = (permissions.AllowAny,)

    pagination_class = BasicPagination

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user)
