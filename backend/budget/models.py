from django.db import models
from events.models import Event


class BudgetItem(models.Model):
    CATEGORY_CHOICES = [
        ('venue', 'Venue & Logistics'),
        ('catering', 'Catering'),
        ('marketing', 'Marketing & Promotion'),
        ('equipment', 'Equipment & Tech'),
        ('decoration', 'Decoration'),
        ('speaker', 'Speaker & Honorarium'),
        ('transport', 'Transport'),
        ('misc', 'Miscellaneous'),
    ]

    STATUS_CHOICES = [
        ('estimated', 'Estimated'),
        ('approved', 'Approved'),
        ('spent', 'Spent'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='budget_items')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='estimated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description} — ₹{self.amount}"
