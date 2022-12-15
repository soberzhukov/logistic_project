from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from common.models import SavedSearch
from common.serializers import GetSavedSearchSerializer, CreateDeleteSavedSearchSerializer
from logisticproject.utils import BasicPagination


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
