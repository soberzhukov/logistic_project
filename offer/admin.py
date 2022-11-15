from django.contrib import admin

from offer.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'name', 'date_created']
