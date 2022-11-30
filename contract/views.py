# from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet

# from logisticproject.utils import BasicPagination
# from payment.serializers import GetContractSerializer, UpdateContractSerializer
# from users.permissions import IsAuthor
#
#
# class CRUDContractViewSet(ModelViewSet):
#     queryset = Contract.objects.all()
#     serializer_class = GetContractSerializer
#     permission_classes = (permissions.IsAuthenticated, IsAuthor)
#     pagination_class = BasicPagination
#
#     def get_serializer_class(self):
#         return GetContractSerializer if self.action in ['list', 'retrieve', 'create'] else UpdateContractSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter()