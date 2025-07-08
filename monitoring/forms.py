from django import forms
from .models import PurchaseOrder, ManpowerDetail
from .mixins import UniqueFieldValidationMixin


class PurchaseOrderForm(UniqueFieldValidationMixin, forms.ModelForm):
    purchase_order = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Purchase Order #", "class": "form-control"}), label="PURCHASE ORDER NO:")
    purchase_order_received = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "P.O Received"}), label="P.O RECEIVED:")
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
    classification = forms.ChoiceField(
    choices=[('', '-- Select Classification --')] + PurchaseOrder.CLASSIFICATION_CHOICES,
    widget=forms.Select(attrs={"class": "form-control"}),
    label="CLASSIFICATION"
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Description", "class": "form-control", "rows": 3}), label="DESCRIPTION/CATEGORY:")
    service_report_number= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Service Report No.", "class": "form-control"}), label="SERVICE REPORT NO:", required=False)
    date_started = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Date Started"}), label="DATE STARTED:", required=False)
    target_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Target Date"}), label="TARGET DATE:")
    completion_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Completion Date"}), label="COMPLETION DATE:", required=False)
    coc_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter COC No.", "class": "form-control"}), label="COC NO:", required=False)
    dr_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter DR No.", "class": "form-control"}), label="DELIVERY RECEIPT NO.", required=False)
    invoice_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Invoice No.", "class": "form-control"}), label="INVOICE NO.", required=False)
    remarks = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Remarks", "class": "form-control", "rows": 3}), label="REMARKS:", required=False)

    unique_fields = ['purchase_order']

    class Meta:
        model = PurchaseOrder
        fields = ['purchase_order', 'purchase_order_received', 'customer_branch', 'total_days', 'manpower', 'time_total', 'classification', 'description', 'service_report_number', 'date_started', 'target_date', 'completion_date', 'coc_number', 'dr_number', 'invoice_number', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Your custom queryset logic
        self.fields['customer_branch'].queryset = PurchaseOrder._meta.get_field('customer_branch').remote_field.model.objects.all()

        # Add 'is-invalid' class to any fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                css = field.widget.attrs.get("class", "")
                if "is-invalid" not in css:
                    field.widget.attrs["class"] = f"{css} is-invalid"


  
