from django.contrib import admin

from common.models import SavedSearch, Image


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'type_search', 'date_create']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'date_created']
