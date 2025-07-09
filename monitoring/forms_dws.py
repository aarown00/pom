# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import DailyWorkStatus, PurchaseOrder

class DailyWorkStatusForm(forms.ModelForm):
    class Meta:
        model = DailyWorkStatus
        fields = ['date', 'manpower', 'time_total']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

DailyWorkStatusFormSet = inlineformset_factory(
    PurchaseOrder,
    DailyWorkStatus,
    form=DailyWorkStatusForm,
    extra=7,           # show up to 7 forms (for adding new)
    max_num=7,
    can_delete=False,
    validate_min=False,
    validate_max=True,
)

