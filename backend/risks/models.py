from django.db import models
from events.models import Event
from django.contrib.auth.models import User


class Risk(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('mitigated', 'Mitigated'),
        ('closed', 'Closed'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='risks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    mitigation_plan = models.TextField(blank=True, help_text="Steps to mitigate the risk")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_risks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-severity', '-created_at']

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"

    @property
    def severity_color(self):
        colors = {'low': '#006d4a', 'medium': '#e6a817', 'high': '#d4620e', 'critical': '#ac3149'}
        return colors.get(self.severity, '#757c7f')
