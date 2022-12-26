from django.contrib import admin

from selection.models import SelectionOffer, SelectionOrder


@admin.register(SelectionOrder)
class SelectionOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sorting_number', 'date_created']


@admin.register(SelectionOffer)
class SelectionOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sorting_number', 'date_created']