from django.contrib import admin
from .models import BudgetItem

@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('event', 'category', 'description', 'amount', 'status')
    list_filter = ('category', 'status')
