from rest_framework.pagination import PageNumberPagination

class BasicPagination(PageNumberPagination):
    page_size = 10
