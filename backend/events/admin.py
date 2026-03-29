from django.contrib import admin
from .models import Event, Resource, EventResource

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'date', 'organizer')
    list_filter = ('status', 'category', 'date')
    search_fields = ('name', 'description')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'capacity', 'is_available')
    list_filter = ('resource_type', 'is_available')

@admin.register(EventResource)
class EventResourceAdmin(admin.ModelAdmin):
    list_display = ('event', 'resource', 'role', 'quantity')
