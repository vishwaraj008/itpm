from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from events.models import Event
from budget.models import BudgetItem
from risks.models import Risk
import json


@login_required
def dashboard_view(request):
    events = Event.objects.all()
    total_events = events.count()
    upcoming = events.filter(status='planned').count()
    in_progress = events.filter(status='in_progress').count()
    total_spent = BudgetItem.objects.aggregate(t=Sum('amount'))['t'] or 0
    open_risks = Risk.objects.filter(status='open').count()

    recent_events = events[:5]

    # Chart data for dashboard
    status_data = dict(events.values_list('status').annotate(count=Count('id')))
    budget_by_event = list(
        events.filter(estimated_budget__gt=0).values('name', 'estimated_budget')
        .annotate(spent=Sum('budget_items__amount'))[:6]
    )

    context = {
        'total_events': total_events,
        'upcoming': upcoming,
        'in_progress': in_progress,
        'total_spent': total_spent,
        'open_risks': open_risks,
        'recent_events': recent_events,
        'status_data': json.dumps(status_data),
        'budget_chart_labels': json.dumps([b['name'][:15] for b in budget_by_event]),
        'budget_chart_estimated': json.dumps([float(b['estimated_budget']) for b in budget_by_event]),
        'budget_chart_spent': json.dumps([float(b['spent'] or 0) for b in budget_by_event]),
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]
