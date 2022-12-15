from common.filters import ObjectFilter
from order.models import Order


class OrderFilter(ObjectFilter):
    class Meta(ObjectFilter.Meta):
        model = Order
