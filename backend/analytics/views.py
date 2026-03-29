from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from events.models import Event
from budget.models import BudgetItem
from risks.models import Risk
import json


@login_required
def analytics_dashboard(request):
    # Status distribution
    status_data = dict(Event.objects.values_list('status').annotate(count=Count('id')))
    # Category distribution
    category_data = dict(Event.objects.values_list('category').annotate(count=Count('id')))
    # Budget by category
    budget_by_cat = dict(
        BudgetItem.objects.values_list('category').annotate(total=Sum('amount'))
    )
    # Monthly events (for line chart)
    from django.db.models.functions import TruncMonth
    monthly = (
        Event.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_labels = [m['month'].strftime('%b %Y') for m in monthly] if monthly else []
    monthly_values = [m['count'] for m in monthly] if monthly else []

    # Risk severity
    risk_severity = dict(Risk.objects.filter(status='open').values_list('severity').annotate(count=Count('id')))

    context = {
        'status_data': json.dumps(status_data),
        'category_data': json.dumps(category_data),
        'budget_by_cat': json.dumps({k: float(v) for k, v in budget_by_cat.items()}),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_values': json.dumps(monthly_values),
        'risk_severity': json.dumps(risk_severity),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(status='planned').count(),
        'total_budget': BudgetItem.objects.aggregate(t=Sum('amount'))['t'] or 0,
        'open_risks': Risk.objects.filter(status='open').count(),
    }
    return render(request, 'analytics/analytics.html', context)
