from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_overview, name='budget_overview'),
    path('event/<int:event_id>/', views.budget_detail, name='budget_detail'),
    path('event/<int:event_id>/add/', views.budget_create, name='budget_create'),
    path('item/<int:item_id>/edit/', views.budget_edit, name='budget_edit'),
    path('item/<int:item_id>/delete/', views.budget_delete, name='budget_delete'),
]
