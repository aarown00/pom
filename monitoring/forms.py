from django import forms
from .models import PurchaseOrder
from .mixins import UniqueFieldValidationMixin, DashCharFieldMixin, SingleSpaceValidationMixin
from django.utils.timezone import localdate


class PurchaseOrderForm(UniqueFieldValidationMixin, DashCharFieldMixin, SingleSpaceValidationMixin, forms.ModelForm):
    purchase_order = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Purchase Order #", "class": "form-control"}), label="PURCHASE ORDER NO:")
    purchase_order_received = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), label="RECEIVED DATE:")
    customer_branch = forms.ModelChoiceField(
     queryset=None, 
     widget=forms.Select(attrs={
            "class": "selectpicker form-control",   
            "data-live-search": "true",
            'title': 'Select Customer',
        }),
     label="CUSTOMER/ADDRESS:",
     empty_label=None,
    )
    classification = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Classification", "class": "form-control"}), label="CLASSIFICATION:")
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Description", "class": "form-control", "rows": 3}), label="DESCRIPTION/CATEGORY:")
    service_report_number= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Service Report No.", "class": "form-control"}), label="SR NO:", required=False)
    date_started = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), label="STARTED DATE:", required=False)
    target_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), label="TARGET DATE:")
    completion_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "max": localdate().isoformat()}), label="COMPLETION DATE:", required=False)
    coc_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter COC No.", "class": "form-control"}), label="COC NO:", required=False)
    dr_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter DR No.", "class": "form-control"}), label="DR NO.", required=False)
    invoice_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Invoice No.", "class": "form-control"}), label="INV NO.", required=False)
    remarks = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter Remarks", "class": "form-control", "rows": 3}), label="REMARKS:", required=False)

    unique_fields = ['purchase_order']
    dash_fields = ['purchase_order', 'classification', 'coc_number', 'dr_number', 'invoice_number', 'service_report_number']
    single_space_fields = ['purchase_order', 'classification', 'description', 'remarks', 'coc_number', 'dr_number', 'invoice_number', 'service_report_number']

    class Meta:
        model = PurchaseOrder
        fields = ['purchase_order', 'purchase_order_received', 'customer_branch', 'classification', 'description', 'service_report_number', 'date_started', 'target_date', 'completion_date', 'coc_number', 'dr_number', 'invoice_number', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fix queryset: sort by customer_name and branch_name
        self.fields['customer_branch'].queryset = (
        PurchaseOrder._meta.get_field('customer_branch')
        .remote_field.model.objects.all()
        .order_by('customer_name', 'branch_name')
        )

        # Add 'is-invalid' class to any fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                css = field.widget.attrs.get("class", "")
                if "is-invalid" not in css:
                    field.widget.attrs["class"] = f"{css} is-invalid"


  
