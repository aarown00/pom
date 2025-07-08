from django import forms
from .models import ManpowerDetail
from .mixins import UniqueFieldValidationMixin


class ManpowerDetailForm(UniqueFieldValidationMixin, forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Manpower Name:", "class": "form-control"}), label="MANPOWER NAME:")
    category = forms.ChoiceField(
    choices=[('', '-- Select Category --')] + ManpowerDetail.CATEGORY_CHOICES,
    widget=forms.Select(attrs={"class": "form-control"}),
    label="CATEGORY"
    )

    unique_fields = ['name']
  
    class Meta:
        model = ManpowerDetail
        fields = ['name', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add 'is-invalid' class to any fields with errors
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                css = field.widget.attrs.get("class", "")
                if "is-invalid" not in css:
                    field.widget.attrs["class"] = f"{css} is-invalid"
    
