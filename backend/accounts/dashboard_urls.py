from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    context = {
        'user_role': request.user.userprofile.get_role_display(),
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]
