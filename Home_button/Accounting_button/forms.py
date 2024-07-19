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



from django import forms
from .models import WorkType

class WorkTypeForm(forms.ModelForm):
    class Meta:
        model = WorkType
        fields = ['name', 'time_norm', 'work_type_group', 'tariff_name', 'job_description', 'hide_in_list']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Поле ввода для наименования
            'time_norm': forms.NumberInput(attrs={'class': 'form-control'}),  # Поле ввода для нормы времени
            'work_type_group': forms.Select(attrs={'class': 'form-control'}),  # Выпадающий список для группы видов работ
            'tariff_name': forms.Select(attrs={'class': 'form-control'}),  # Выпадающий список для имени тарифа
            'job_description': forms.Textarea(attrs={'class': 'form-control'}),  # Текстовое поле для описания работы
            'hide_in_list': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Чекбокс для скрытия в списке
        }







from django import forms
from .models import StandardOperationsJournal

class StandardOperationsJournalForm(forms.ModelForm):
    class Meta:
        model = StandardOperationsJournal
        fields = ['work_type', 'quantity']  # Только редактируемые поля

    def __init__(self, *args, **kwargs):
        super(StandardOperationsJournalForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.CharField(
            initial=self.instance.group if self.instance else '',
            disabled=True,
            label='Group'
        )
        self.fields['time_norm'] = forms.CharField(
            initial=self.instance.time_norm if self.instance else '',
            disabled=True,
            label='Time Norm'
        )
        self.fields['tariff'] = forms.CharField(
            initial=self.instance.tariff if self.instance else '',
            disabled=True,
            label='Tariff'
        )
        self.fields['total_time'] = forms.CharField(
            initial=self.instance.total_time if self.instance else '',
            disabled=True,
            label='Total Time'
        )
        self.fields['total_cost'] = forms.CharField(
            initial=self.instance.total_cost if self.instance else '',
            disabled=True,
            label='Total Cost'
        )
