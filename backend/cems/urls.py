"""CEMS URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('budget/', include('budget.urls')),
    path('risks/', include('risks.urls')),
    path('analytics/', include('analytics.urls')),
    path('ai/', include('ai_features.urls')),
    path('dashboard/', include('accounts.dashboard_urls')),
    path('', lambda request: redirect('/dashboard/' if request.user.is_authenticated else '/accounts/login/')),
]
