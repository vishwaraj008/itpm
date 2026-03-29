from django.urls import path
from . import views
from . import pdf_views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics'),
    path('export/analytics/', pdf_views.export_analytics_pdf, name='export_analytics_pdf'),
    path('export/event/<int:event_id>/', pdf_views.export_event_pdf, name='export_event_pdf'),
]
