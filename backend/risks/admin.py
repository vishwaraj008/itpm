from django.contrib import admin
from .models import Risk

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'severity', 'status', 'owner')
    list_filter = ('severity', 'status')
