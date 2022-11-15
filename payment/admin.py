from django.contrib import admin

from payment.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'count']
