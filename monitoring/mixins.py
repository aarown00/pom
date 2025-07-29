# mixins.py
from .models import CustomerDetail 
import re

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


class NormalizedCustomerNameUniqueMixin:
    """
    Validates that `customer_name` is unique after normalization:
    - Lowercase
    - Remove all non-alphanumeric characters (spaces, dashes, punctuation, etc.)
    - Blocks special characters from input
    """

    def normalize_name(self, name):
        return re.sub(r'[^a-z0-9]', '', name.lower())

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')

        if customer_name:
            # ❌ Reject if contains special characters (only allow letters, numbers, spaces)
            if not re.fullmatch(r'[A-Za-z0-9 ]+', customer_name):
                self.add_error(
                    'customer_name',
                    'Special characters are not allowed in customer name.'
                )
                return cleaned_data  # Skip further checks if invalid format

            normalized_input = self.normalize_name(customer_name)
            qs = self._meta.model.objects.all()

            for obj in qs:
                if customer_name == obj.customer_name:
                    # Exact match — allow
                    continue
                existing_normalized = self.normalize_name(obj.customer_name)
                if normalized_input == existing_normalized:
                    self.add_error(
                        'customer_name',
                        f'The customer name already exists. Please use the exact existing: "{obj.customer_name}".'
                    )
                    break

        return cleaned_data
    
class UniqueBranchUnderCustomerMixin:
    """
    - Validates that branch_name is unique under the same customer after normalization
    - Blocks special characters in branch_name (allows only letters, numbers, spaces)
    """

    def normalize_name(self, name):
        return re.sub(r'[^a-z0-9]', '', name.lower())

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')
        branch_name = cleaned_data.get('branch_name')

        if customer_name and branch_name:
            # ❌ Reject if branch_name contains special characters (allow only letters, numbers, spaces)
            if not re.fullmatch(r'[A-Za-z0-9 ]+', branch_name):
                self.add_error(
                    'branch_name',
                    'Special characters are not allowed in branch name.'
                )
                return cleaned_data  # Skip further checks if invalid

            normalized_branch = self.normalize_name(branch_name)
            normalized_customer = customer_name.strip().lower()

            qs = CustomerDetail.objects.all()
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for obj in qs:
                if obj.customer_name.strip().lower() == normalized_customer:
                    existing_branch_normalized = self.normalize_name(obj.branch_name)
                    if existing_branch_normalized == normalized_branch:
                        self.add_error(
                            'branch_name',
                            f'The branch "{obj.branch_name}" already exists under customer "{obj.customer_name}".'
                        )
                        break

        return cleaned_data

