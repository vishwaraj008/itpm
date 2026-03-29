from django import forms
from .models import Risk


class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['title', 'description', 'severity', 'status', 'mitigation_plan', 'owner']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control cf-form-control', 'placeholder': 'Risk title'}),
            'description': forms.Textarea(attrs={'class': 'form-control cf-form-control', 'rows': 3, 'placeholder': 'Describe the risk...'}),
            'severity': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'status': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'mitigation_plan': forms.Textarea(attrs={'class': 'form-control cf-form-control', 'rows': 3, 'placeholder': 'Mitigation steps...'}),
            'owner': forms.Select(attrs={'class': 'form-select cf-form-select'}),
        }
