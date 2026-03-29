from django import forms
from .models import BudgetItem


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['category', 'description', 'amount', 'status']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select cf-form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control cf-form-control', 'placeholder': 'e.g. Speaker fee for Dr. Smith'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control cf-form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select cf-form-select'}),
        }
