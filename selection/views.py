from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from logisticproject.utils import BasicPagination
from selection.models import SelectionOffer, SelectionOrder
from selection.serializers import SelectionOfferSerializer, SelectionOrderSerializer


class SelectionObjectReadOnlyViewSet(ReadOnlyModelViewSet):
    """"""
    permission_classes = (AllowAny,)
    pagination_class = BasicPagination


class SelectionOrderReadOnlyViewSet(SelectionObjectReadOnlyViewSet):
    queryset = SelectionOrder.objects.all()
    serializer_class = SelectionOrderSerializer

class SelectionOfferReadOnlyViewSet(SelectionObjectReadOnlyViewSet):
    queryset = SelectionOffer.objects.all()
    serializer_class = SelectionOfferSerializer