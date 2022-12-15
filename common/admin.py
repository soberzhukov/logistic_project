from django.contrib import admin

from common.models import SavedSearch


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'type_search', 'date_create']
