from django.contrib import admin

from contract.models import Contract


@admin.register(Contract)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
