from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomerDetail(models.Model):
    customer_name = models.CharField(max_length=200)
    branch_name = models.TextField()

    def __str__(self):
        return f"{self.customer_name} - {self.branch_name}"
    
class ManpowerDetail(models.Model):
    CATEGORY_CHOICES = [
        ('Employee', 'Employee'),
        ('Contractor', 'Contractor'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Check if this manpower is linked to any PurchaseOrder
        if self.purchaseorder_set.exists():
            raise ValidationError(f"Cannot delete '{self.name}' because it is used in existing P.O's")
        super().delete(*args, **kwargs)


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled'),
    ]

    CLASSIFICATION_CHOICES= [
        ('GENSET A', 'GENSET A'),
        ('GENSET B', 'GENSET B'),
        ('GENSET C', 'GENSET C'),
    ]

    MANPOWER_TYPE_CHOICES = [
        ('Employee Based', 'Employee Based'),
        ('Contractor Based', 'Contractor Based'),
        ('Employee & Contractor Based', 'Employee & Contractor Based'),
    ]

    id = models.AutoField(primary_key=True)
    date_recorded = models.DateField(auto_now_add=True)

    purchase_order = models.CharField(max_length=100, unique=True)
    purchase_order_received = models.DateField()
    customer_branch = models.ForeignKey(CustomerDetail, on_delete=models.PROTECT)

    total_days = models.PositiveIntegerField(blank=True, null=True)
    manpower = models.ManyToManyField(ManpowerDetail, blank=True)
    manpower_total = models.PositiveIntegerField(default=0, editable=False)
    manpower_type = models.CharField(max_length=30, choices=MANPOWER_TYPE_CHOICES, blank=True, null=True, editable=False)
    time_total = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        today = timezone.now().date()

        # Respect existing Cancelled status — do not change it
        if self.status == 'Cancelled':
            super().save(*args, **kwargs)
            return

        self.target_date_delayed = 0

        # Priority 1: Completed if finished today
        if self.completion_date == today:
            self.status = 'Completed'

        # Priority 2: Delayed if past target and not completed
        elif self.target_date < today and not self.completion_date:
            self.status = 'Delayed'
            self.target_date_delayed = (today - self.target_date).days 

        # Priority 3: Ongoing if started today
        elif self.date_started == today:
            self.status = 'Ongoing'

        # Priority 4: Pending if start is in future or not set
        elif not self.date_started or self.date_started > today:
            self.status = 'Pending'

        # Save temporarily first to create an instance (required for m2m)
        super().save(*args, **kwargs)

        # Then update the count based on selected manpower
        self.manpower_total = self.manpower.count()

        super().save(update_fields=['manpower_total'])

    @property
    def total_work_hour(self):
        if self.manpower_total is not None and self.time_total is not None:
            return self.manpower_total * self.time_total
        return None

    classification = models.CharField(max_length=100, choices=CLASSIFICATION_CHOICES)
    description = models.TextField()
    service_report_number = models.CharField(blank=True, null=True)
    date_started = models.DateField(blank=True, null=True)
    target_date = models.DateField()
    target_date_delayed = models.PositiveIntegerField(default=0)
    completion_date = models.DateField(blank=True, null=True)
    coc_number = models.CharField(max_length=100, blank=True, null=True)
    dr_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True, default='Pending')

    def __str__(self):
        return f"{self.purchase_order}"
    
    def customer(self):
        return f"{self.customer_branch.customer_name} - {self.customer_branch.branch_name}"
    customer.short_description = 'Customer'

@receiver(m2m_changed, sender=PurchaseOrder.manpower.through)
def update_manpower_fields(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        manpower = instance.manpower.all()
        instance.manpower_total = manpower.count()

        has_employee = manpower.filter(category='Employee').exists()
        has_contractor = manpower.filter(category='Contractor').exists()

        if has_employee and has_contractor:
            instance.manpower_type = 'Employee & Contractor Based'
        elif has_employee:
            instance.manpower_type = 'Employee Based'
        elif has_contractor:
            instance.manpower_type = 'Contractor Based'
        else:
            instance.manpower_type = None

        instance.save(update_fields=['manpower_total', 'manpower_type'])

