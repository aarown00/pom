from django import forms
from .models import CustomerDetail


class CustomerDetailForm(forms.ModelForm):
    customer_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Customer Name:", "class": "form-control"}), label="CUSTOMER NAME:")
    branch_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Branch/Address:", "class": "form-control"}), label="BRANCH NAME:")
  

    class Meta:
        model = CustomerDetail
        fields = ['customer_name', 'branch_name']
