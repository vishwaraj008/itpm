from django.urls import path
from . import views

urlpatterns = [
    path('', views.risk_list, name='risk_list'),
    path('event/<int:event_id>/add/', views.risk_create, name='risk_create'),
    path('<int:risk_id>/edit/', views.risk_edit, name='risk_edit'),
    path('<int:risk_id>/delete/', views.risk_delete, name='risk_delete'),
]
