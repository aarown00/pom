from django import forms
from .models import CustomerDetail


class CustomerDetailForm(forms.ModelForm):
    customer_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Customer Name:", "class": "form-control"}), label="CUSTOMER NAME:")
    branch_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Branch/Address:", "class": "form-control"}), label="BRANCH NAME:")
  

    class Meta:
        model = CustomerDetail
        fields = ['customer_name', 'branch_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add 'is-invalid' class to any fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                css = field.widget.attrs.get("class", "")
                if "is-invalid" not in css:
                    field.widget.attrs["class"] = f"{css} is-invalid"
