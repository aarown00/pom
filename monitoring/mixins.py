# mixins.py
from django import forms
from django.db.models import Q

class UniqueFieldValidationMixin:
    """
    Mixin for ModelForms to validate that specific fields are unique (case-insensitive).
    Set `unique_fields = ['field1', 'field2']` in your form class.
    """

    def clean(self):
        cleaned_data = super().clean()
        for field_name in getattr(self, 'unique_fields', []):
            value = cleaned_data.get(field_name)

            if value is None:
                continue

            # Case-insensitive filter using __iexact
            lookup = {f"{field_name}__iexact": value}
            qs = self._meta.model.objects.filter(**lookup)

            # Exclude current record if editing
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error(field_name, f"This {field_name.replace('_', ' ')} already exists.")
        return cleaned_data
