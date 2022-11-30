from django.contrib import admin

from offer.models import Offer, ElectedOffer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'name', 'date_created']


@admin.register(ElectedOffer)
class ElectedOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'offer', 'notes']
