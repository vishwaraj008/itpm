from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_dashboard, name='ai_dashboard'),
    path('generate-description/', views.generate_description, name='ai_generate_description'),
    path('smart-schedule/', views.smart_schedule, name='ai_smart_schedule'),
    path('estimate-budget/', views.estimate_budget, name='ai_estimate_budget'),
]
