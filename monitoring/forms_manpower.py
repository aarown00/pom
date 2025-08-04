from django import forms
from .models import ManpowerDetail
from .mixins import UniqueFieldValidationMixin, LetterCharFieldMixin, SingleSpaceValidationMixin


class ManpowerDetailForm(UniqueFieldValidationMixin, LetterCharFieldMixin, SingleSpaceValidationMixin, forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter Manpower Name:", "class": "form-control"}), label="MANPOWER NAME:")
    category = forms.ChoiceField(
    choices=ManpowerDetail.CATEGORY_CHOICES,
     widget=forms.Select(attrs={
            "class": "selectpicker form-control",   
            'title': 'Select Category',
        }),
     label="CATEGORY:",
    )

    unique_fields = ['name']
    letter_fields = ['name']
    single_space_fields = ['name']
  
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

    def clean(self):
        cleaned = super().clean()

        # Protect category from being changed during edit
        if self.instance.pk:
            original = type(self.instance).objects.get(pk=self.instance.pk)
            if cleaned.get('category') != original.category:
                self.add_error('category', 'You cannot change the category.')

        return cleaned

    
