from django.db.models import Count, F
from rest_framework import permissions, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common.models import SavedSearch
from common.serializers import GetSavedSearchSerializer, CreateDeleteSavedSearchSerializer
from logisticproject.utils import BasicPagination
from users.permissions import IsObjectAuthor


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


class CRUDObjectViewSet(ModelViewSet):
    """CRUD without create"""
    permission_classes = (IsObjectAuthor,)
    pagination_class = BasicPagination
    read_action_list = ['list', 'retrieve', 'create']

    def create(self, request, *args, **kwargs):
        """Пост запрос возвращает список"""
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        # пользователь может обновлять и удалять только свои объекты
        if self.request.method not in ['POST', 'GET']:
            return self.queryset.filter(author=self.request.user)

        contracts_field = kwargs.get('contracts_field')
        queryset = self.queryset.annotate(count_cs=Count(contracts_field)).filter(
            max_contracts__gt=F('count_cs')).exclude(status='draft')
        if self.request.user.is_authenticated and self.action == 'retrieve':
            # авторизованный пользователь может получить свой объект, даже если количество контракторов заполнено
            queryset = queryset | self.queryset.filter(author=self.request.user)
        elif self.request.user.is_authenticated:
            # исключаю из списка объекты автора
            queryset = queryset.exclude(author=self.request.user)
        return queryset.distinct()


class CounterObjectAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count_views += 1
        instance.save()
        return Response(data={'message': 'ok'}, status=HTTP_200_OK)


class ElectedViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BasicPagination
    read_action_list = ['list', 'retrieve']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
