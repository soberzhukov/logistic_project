from django.contrib import admin

from order.models import Order, ElectedOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'name', 'date_created']





@admin.register(ElectedOrder)
class ElectedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'notes']
