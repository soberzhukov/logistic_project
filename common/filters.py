from django.db.models import Q
from django_filters import rest_framework as filters

from payment.models import PaymentMethod, Currency


class ObjectFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='icontains')
    budgets__count = filters.RangeFilter()
    budgets__currency = filters.ModelMultipleChoiceFilter(field_name='budgets__currency__short_title',
                                                         to_field_name='short_title',
                                                         queryset=Currency.objects.all())
    payment_methods = filters.ModelMultipleChoiceFilter(field_name='payment_methods__title', to_field_name='title',
                                                       queryset=PaymentMethod.objects.all())
    q = filters.CharFilter(method='search')

    sort = filters.Filter(method='sorting_method')
    ordering_fields = ['execution_time', 'date_created', 'max_contracts', 'count_views']

    class Meta:
        model = None
        fields = ['name', 'description', 'status', 'payment_methods', 'execution_time', 'date_created', 'max_contracts',
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

    def sorting_method(self, queryset, name, value):
        def term_valid(term):
            if term.startswith("-"):
                term = term[1:]
            return term in self.ordering_fields

        ordering = [term for term in value if term_valid(term)]
        return queryset.order_by(*ordering)
