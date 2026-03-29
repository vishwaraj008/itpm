from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('technical', 'Technical'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    expected_attendees = models.PositiveIntegerField(default=0)
    estimated_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    @property
    def total_spent(self):
        return self.budget_items.aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def remaining_budget(self):
        return self.estimated_budget - self.total_spent

    @property
    def is_overspent(self):
        return self.total_spent > self.estimated_budget

    @property
    def open_risks_count(self):
        return self.risks.filter(status='open').count()


class Resource(models.Model):
    TYPE_CHOICES = [
        ('venue', 'Venue'),
        ('equipment', 'Equipment'),
    ]

    name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.PositiveIntegerField(default=0, help_text="Capacity (seats for venue, quantity for equipment)")
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

    def is_booked_on(self, date, start_time, end_time, exclude_event=None):
        """Check if resource is booked for a given date/time range."""
        bookings = self.event_resources.filter(
            event__date=date,
            event__start_time__lt=end_time,
            event__end_time__gt=start_time,
        )
        if exclude_event:
            bookings = bookings.exclude(event=exclude_event)
        return bookings.exists()


class EventResource(models.Model):
    ROLE_CHOICES = [
        ('venue', 'Venue'),
        ('equipment', 'Equipment'),
        ('volunteer', 'Volunteer'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_resources')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='event_resources')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='equipment')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['event', 'resource']

    def __str__(self):
        return f"{self.resource.name} → {self.event.name}"
