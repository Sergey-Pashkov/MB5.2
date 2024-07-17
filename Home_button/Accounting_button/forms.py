from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['short_name', 'full_name', 'contract_price', 'contract_number_date', 'inn', 'nomenclature_units', 'tax_system', 'activity_types', 'contact_name', 'phone_number', 'email', 'postal_address', 'comment', 'hide_in_list']
        widgets = {
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.Textarea(attrs={'class': 'form-control'}),
            'contract_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'contract_number_date': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'nomenclature_units': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_system': forms.Select(attrs={'class': 'form-control'}),
            'activity_types': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'postal_address': forms.Textarea(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'hide_in_list': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from django import forms
from .models import WorkTypeGroup

# Форма для модели WorkTypeGroup с Bootstrap стилизацией
class WorkTypeGroupForm(forms.ModelForm):
    class Meta:
        model = WorkTypeGroup
        fields = ['name', 'comments', 'hide_in_list']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'hide_in_list': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

