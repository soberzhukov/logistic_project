from django.db.models import Q
from django_filters import rest_framework as filters

from order.models import Order


class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='icontains')
    payment_method = filters.CharFilter(field_name='payment_method', lookup_expr='icontains')
    # execution_time = filters.DateTimeFilter(field_name='execution_time', lookup_expr='icontains')
    # date_created = filters.DateTimeFilter(field_name='date_created', lookup_expr='icontains')
    q = filters.CharFilter(method='search')
    # sort = filters.Filter(method='sorting_method')
    ordering_fields = ['status', 'payment_method', 'execution_time', 'date_created', 'max_contracts', 'count_views']

    class Meta:
        model = Order
        fields = ['name', 'description', 'status', 'payment_method', 'execution_time', 'date_created', 'max_contracts',
                  'count_views']

    def filter_queryset(self, queryset):
        data = self.get_data()
        FORM = self.get_form_class()
        form = FORM(data=data)
        form.is_valid()
        for name, value in form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
        return queryset

    def get_data(self):
        return self.request.data.copy()

    def search(self, queryset, name, value):
        if value:
            queryset = queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
        return queryset
