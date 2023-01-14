from django.contrib import admin

from common.models import SavedSearch, File


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'type_search', 'date_create']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'date_created']
