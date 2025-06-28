from django import forms
from .models import PurchaseOrder, ManpowerDetail



class PurchaseOrderForm(forms.ModelForm):
    purchase_order = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Purchase Order #", "class": "form-control"}), label="PURCHASE ORDER:")
    date_in_email = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Date in Email"}), label="DATE IN EMAIL:")
    customer_branch = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={"class": "form-control"}), label="CUSTOMER/ADDRESS:")
    total_days = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Enter # of Total Days", "class": "form-control"}), label="TOTAL DAYS (PI):", required=False)
    manpower = forms.ModelMultipleChoiceField(
        queryset=ManpowerDetail.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'selectpicker',
            'data-live-search': 'true',
            'data-actions-box': 'true',
            'data-selected-text-format': 'count > 1',
            'title': 'Select Manpower/s',
        }),
        label="MANPOWER (M):",
        required=False
    )
    time_total = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Enter Time Total", "class": "form-control"}), label="TIME TOTAL (T):", required=False)
    item_model = forms.ChoiceField(
    choices=[('', '-- Select Model --')] + PurchaseOrder.ITEM_MODEL_CHOICES,
    widget=forms.Select(attrs={"class": "form-control"}),
    label="Select Model"
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Description", "class": "form-control", "rows": 3}), label="DESCRIPTION:")
    service_report= forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Report/s", "class": "form-control", "rows": 3}), label="SERVICE REPORTS/S:", required=False)
    date_started = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Date Started"}), label="DATE STARTED:", required=False)
    target_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Target Date"}), label="TARGET DATE:")
    

    class Meta:
        model = PurchaseOrder
        fields = ['purchase_order', 'date_in_email', 'customer_branch', 'total_days', 'manpower', 'time_total', 'item_model', 'description', 'service_report', 'date_started', 'target_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the customer_branch queryset
        self.fields['customer_branch'].queryset = PurchaseOrder._meta.get_field('customer_branch').remote_field.model.objects.all()
