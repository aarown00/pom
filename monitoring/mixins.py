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

            if not value:
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
    Validates that `customer_name` is unique after normalization,
    except:
      * Exact same string duplicates are allowed (e.g., multiple "KFC" if "KFC" exists).
      * Editing the same instance with case-only change is allowed even if others exist.
    """

    def normalize_name(self, name):
        return re.sub(r'[^a-z0-9]', '', name.lower())

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')

        if customer_name:
            # Reject if contains disallowed special characters
            if not re.fullmatch(r'[A-Za-z0-9 ]+', customer_name):
                self.add_error(
                    'customer_name',
                    'Special characters are not allowed in this field.'
                )
                return cleaned_data  # skip further checks

            # If editing and only case changed from original, allow it
            if (
                getattr(self, 'instance', None)
                and self.instance.pk
                and self.instance.customer_name
                and self.instance.customer_name.lower() == customer_name.lower()
            ):
                return cleaned_data  # case-only edit of an existing value is allowed

            normalized_input = self.normalize_name(customer_name)

            # Base queryset excluding self if editing
            qs = self._meta.model.objects.all()
            if getattr(self, 'instance', None) and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            for obj in qs:
                if normalized_input == self.normalize_name(obj.customer_name):
                    # allow exact same string duplicate (e.g., another "KFC" when creating "KFC")
                    if obj.customer_name == customer_name:
                        continue
                    # otherwise it's a conflict (e.g., trying to create "kfc" while "KFC" exists,
                    # or changing to a variant that normalizes to an existing different value)
                    self.add_error(
                        'customer_name',
                        f'The customer already exists: "{obj.customer_name}". '
                        'Use existing (case-sensitive) if you want to add it again.'
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
                    'Special characters are not allowed in this field.'
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


class DashCharFieldMixin:
    """
    Mixin to restrict special characters in specific fields.
    Only allows letters, numbers, spaces, and dashes (-).
    """

    allowed_pattern = re.compile(r'^[\w\s-]+$')  # \w = a-zA-Z0-9 and _

    def clean(self):
        cleaned_data = super().clean()
        for field_name in getattr(self, 'dash_fields', []):
            value = cleaned_data.get(field_name)
            if not value:
                continue

            if not self.allowed_pattern.match(value):
                self.add_error(
                    field_name,
                    f'Only dash and underscore is allowed in this field.'
                )
        return cleaned_data
    
class LetterCharFieldMixin:
    
    allowed_pattern = re.compile(r'^[A-Za-z ]+$')

    def clean(self):
        cleaned_data = super().clean()
        for field_name in getattr(self, 'letter_fields', []):
            value = cleaned_data.get(field_name)
            if not value:
                continue

            if not self.allowed_pattern.match(value):
                self.add_error(
                    field_name,
                    f'Only letters are allowed in this field.'
                )
        return cleaned_data    