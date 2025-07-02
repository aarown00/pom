from django import forms
from .models import ManpowerDetail


class ManpowerDetailForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Manpower Name:", "class": "form-control"}), label="MANPOWER NAME:")
    category = forms.ChoiceField(
    choices=[('', '-- Select Category --')] + ManpowerDetail.CATEGORY_CHOICES,
    widget=forms.Select(attrs={"class": "form-control"}),
    label="CATEGORY"
    )
  
    class Meta:
        model = ManpowerDetail
        fields = ['name', 'category']
