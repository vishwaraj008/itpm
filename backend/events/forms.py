from django import forms
from .models import Event, Resource, EventResource


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'category', 'status', 'date', 'start_time',
                  'end_time', 'venue', 'expected_attendees', 'estimated_budget']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control cf-form-control', 'placeholder': 'Event name'}),
            'description': forms.Textarea(attrs={'class': 'form-control cf-form-control', 'rows': 4, 'placeholder': 'Event description', 'id': 'event-description'}),
            'category': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'status': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control cf-form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control cf-form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control cf-form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control cf-form-control', 'placeholder': 'Venue name'}),
            'expected_attendees': forms.NumberInput(attrs={'class': 'form-control cf-form-control', 'placeholder': '0'}),
            'estimated_budget': forms.NumberInput(attrs={'class': 'form-control cf-form-control', 'placeholder': '0.00'}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'resource_type', 'capacity', 'description', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control cf-form-control', 'placeholder': 'Resource name'}),
            'resource_type': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control cf-form-control', 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control cf-form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EventResourceForm(forms.ModelForm):
    class Meta:
        model = EventResource
        fields = ['resource', 'role', 'quantity']
        widgets = {
            'resource': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'role': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control cf-form-control', 'min': 1}),
        }
