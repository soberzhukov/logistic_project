from django.contrib import admin

from offer.models import Offer
from order.models import Order
from selection.models import SelectionOffer, SelectionOrder

class OrdersInline(admin.TabularInline):
    model = Order.selections_order.through  # noqa

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name != 'orders':
            kwargs["queryset"] = Order.objects.filter(status='published')
        return super().formfield_for_foreignkey(db_field, request=None, **kwargs)


@admin.register(SelectionOrder)
class SelectionOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sorting_number', 'date_created']
    exclude = ['orders']
    inlines = [OrdersInline]

class OffersInline(admin.TabularInline):
    model = Offer.selections_offer.through  # noqa

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name != 'offers':
            kwargs["queryset"] = Offer.objects.filter(status='published')
        return super().formfield_for_foreignkey(db_field, request=None, **kwargs)

@admin.register(SelectionOffer)
class SelectionOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sorting_number', 'date_created']
    exclude = ['offers']
    inlines = [OffersInline]