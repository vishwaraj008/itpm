from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from events.models import Event
from .models import BudgetItem
from .forms import BudgetItemForm
from accounts.decorators import faculty_or_admin_required


@login_required
def budget_overview(request):
    events = Event.objects.annotate(spent_total=Sum('budget_items__amount')).order_by('-date')
    total_estimated = events.aggregate(total=Sum('estimated_budget'))['total'] or 0
    total_spent = BudgetItem.objects.aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'events': events,
        'total_estimated': total_estimated,
        'total_spent': total_spent,
        'remaining': total_estimated - total_spent,
    }
    return render(request, 'budget/budget_overview.html', context)


@login_required
def budget_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    items = event.budget_items.all()
    by_category = {}
    for item in items:
        cat = item.get_category_display()
        by_category[cat] = by_category.get(cat, 0) + float(item.amount)
    context = {
        'event': event,
        'items': items,
        'by_category': by_category,
    }
    return render(request, 'budget/budget_detail.html', context)


@login_required
@faculty_or_admin_required
def budget_create(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.event = event
            item.save()
            messages.success(request, f'Budget item "₹{item.amount}" added.')
            return redirect('budget_detail', event_id=event.id)
    else:
        form = BudgetItemForm()
    return render(request, 'budget/budget_form.html', {'form': form, 'event': event})


@login_required
@faculty_or_admin_required
def budget_edit(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id)
    if request.method == 'POST':
        form = BudgetItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget item updated.')
            return redirect('budget_detail', event_id=item.event.id)
    else:
        form = BudgetItemForm(instance=item)
    return render(request, 'budget/budget_form.html', {'form': form, 'event': item.event, 'editing': True})


@login_required
@faculty_or_admin_required
def budget_delete(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id)
    event_id = item.event.id
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Budget item deleted.')
        return redirect('budget_detail', event_id=event_id)
    return render(request, 'budget/budget_confirm_delete.html', {'item': item})
