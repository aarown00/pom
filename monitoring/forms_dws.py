# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import DailyWorkStatus, PurchaseOrder, ManpowerDetail

class DailyWorkStatusForm(forms.ModelForm):
    manpower = forms.ModelMultipleChoiceField(
        queryset=ManpowerDetail.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'selectpicker form-control',
            'data-live-search': 'true',
            'data-actions-box': 'true',
            'data-selected-text-format': 'count > 1',
            'title': 'Select Manpower/s',
        }),
        label="MANPOWER (M):",
        required=False
    )

    class Meta:
        model = DailyWorkStatus
        fields = ['date', 'manpower', 'time_total', 'itinenary_remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter time total in this day...'}),
            'itinenary_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter job done...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        manpower = cleaned_data.get('manpower')
        time_total = cleaned_data.get('time_total')

        if manpower and manpower.exists() and time_total is None:
            self.add_error('time_total', "Time total is required when manpower is selected.")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply 'is-invalid' class for fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_class} is-invalid".strip()

DailyWorkStatusFormSet = inlineformset_factory(
    PurchaseOrder,
    DailyWorkStatus,
    form=DailyWorkStatusForm,
    extra=15,
    max_num=15,
    can_delete=False,
    validate_min=False,
    validate_max=True,
)
