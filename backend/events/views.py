from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, Resource, EventResource
from .forms import EventForm, ResourceForm, EventResourceForm
from accounts.decorators import faculty_or_admin_required, admin_required


@login_required
def event_list(request):
    events = Event.objects.select_related('organizer').all()

    # Filters
    status = request.GET.get('status')
    category = request.GET.get('category')
    search = request.GET.get('search')

    if status:
        events = events.filter(status=status)
    if category:
        events = events.filter(category=category)
    if search:
        events = events.filter(Q(name__icontains=search) | Q(description__icontains=search))

    context = {
        'events': events,
        'status_choices': Event.STATUS_CHOICES,
        'category_choices': Event.CATEGORY_CHOICES,
        'current_status': status,
        'current_category': category,
        'search_query': search or '',
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event.objects.select_related('organizer'), id=event_id)
    resources = event.event_resources.select_related('resource').all()
    budget_items = event.budget_items.all() if hasattr(event, 'budget_items') else []
    risks = event.risks.all() if hasattr(event, 'risks') else []

    context = {
        'event': event,
        'resources': resources,
        'budget_items': budget_items,
        'risks': risks,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
@faculty_or_admin_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
@faculty_or_admin_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.userprofile.role == 'faculty' and event.organizer != request.user:
        messages.error(request, 'You can only edit your own events.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.name}" updated!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event', 'event': event})


@login_required
@faculty_or_admin_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.userprofile.role == 'faculty' and event.organizer != request.user:
        messages.error(request, 'You can only delete your own events.')
        return redirect('event_list')

    if request.method == 'POST':
        name = event.name
        event.delete()
        messages.success(request, f'Event "{name}" deleted.')
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# --- Resource Views ---

@login_required
@faculty_or_admin_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'events/resource_list.html', {'resources': resources})


@login_required
@faculty_or_admin_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created!')
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'events/resource_form.html', {'form': form, 'title': 'Add Resource'})


@login_required
@faculty_or_admin_required
def assign_resource(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventResourceForm(request.POST)
        if form.is_valid():
            resource = form.cleaned_data['resource']
            # Conflict detection
            if resource.is_booked_on(event.date, event.start_time, event.end_time, exclude_event=event):
                messages.warning(request,
                    f'⚠️ Resource "{resource.name}" is already booked for this date/time! Assignment saved with conflict warning.')
            er = form.save(commit=False)
            er.event = event
            er.save()
            messages.success(request, f'Resource "{resource.name}" assigned to "{event.name}".')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventResourceForm()
    return render(request, 'events/assign_resource.html', {'form': form, 'event': event})
