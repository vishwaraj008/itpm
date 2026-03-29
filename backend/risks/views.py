from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from .models import Risk
from .forms import RiskForm
from accounts.decorators import faculty_or_admin_required


@login_required
def risk_list(request):
    risks = Risk.objects.select_related('event', 'owner').all()
    status_filter = request.GET.get('status')
    severity_filter = request.GET.get('severity')
    if status_filter:
        risks = risks.filter(status=status_filter)
    if severity_filter:
        risks = risks.filter(severity=severity_filter)
    context = {
        'risks': risks,
        'status_choices': Risk.STATUS_CHOICES,
        'severity_choices': Risk.SEVERITY_CHOICES,
        'current_status': status_filter,
        'current_severity': severity_filter,
        'open_count': Risk.objects.filter(status='open').count(),
        'critical_count': Risk.objects.filter(severity='critical', status='open').count(),
    }
    return render(request, 'risks/risk_list.html', context)


@login_required
@faculty_or_admin_required
def risk_create(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.event = event
            if not risk.owner:
                risk.owner = request.user
            risk.save()
            messages.success(request, f'Risk "{risk.title}" added.')
            return redirect('event_detail', event_id=event.id)
    else:
        form = RiskForm()
    return render(request, 'risks/risk_form.html', {'form': form, 'event': event})


@login_required
@faculty_or_admin_required
def risk_edit(request, risk_id):
    risk = get_object_or_404(Risk, id=risk_id)
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Risk updated.')
            return redirect('risk_list')
    else:
        form = RiskForm(instance=risk)
    return render(request, 'risks/risk_form.html', {'form': form, 'event': risk.event, 'editing': True})


@login_required
@faculty_or_admin_required
def risk_delete(request, risk_id):
    risk = get_object_or_404(Risk, id=risk_id)
    event_id = risk.event.id
    if request.method == 'POST':
        risk.delete()
        messages.success(request, 'Risk deleted.')
        return redirect('event_detail', event_id=event_id)
    return render(request, 'risks/risk_confirm_delete.html', {'risk': risk})
