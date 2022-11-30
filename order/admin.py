from django.contrib import admin

from order.models import Order, SavedSearch, ElectedOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'name', 'date_created']


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'type_search', 'date_create']


@admin.register(ElectedOrder)
class ElectedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'notes']
