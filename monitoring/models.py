from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils.timezone import localdate
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
        if self.dailyworkstatus_set.exists():
            raise ValidationError(f"Cannot delete '{self.name}' because it is used in existing itinenary!")
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
        ('employee', 'Employee Based'),
        ('contractor', 'Contractor Based'),
        ('both', 'Employee + Contractor Based'),
    ]

    manpower_type = models.CharField(
        max_length=20,
        choices=MANPOWER_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    id = models.AutoField(primary_key=True)
    date_recorded = models.DateField(auto_now_add=True)
    purchase_order = models.CharField(max_length=100, unique=True)
    purchase_order_received = models.DateField()
    customer_branch = models.ForeignKey(CustomerDetail, on_delete=models.PROTECT)
    total_days = models.PositiveIntegerField(blank=True, null=True)

    manpower_total = models.PositiveIntegerField(default=0, editable=False)
    work_hours_total = models.PositiveIntegerField(default=0, editable=False)
    working_days_total = models.PositiveIntegerField(default=0, editable=False)


    classification = models.CharField(max_length=100, choices=CLASSIFICATION_CHOICES)
    description = models.TextField()
    service_report_number = models.CharField(max_length=100, blank=True, null=True)
    date_started = models.DateField(blank=True, null=True)
    target_date = models.DateField()
    target_date_status = models.CharField(
        max_length=20,
        choices=[("original", "Original"), ("adjusted", "Adjusted")],
        default="original"
    )
    target_date_delayed = models.PositiveIntegerField(default=0)
    completion_date = models.DateField(blank=True, null=True)
    coc_number = models.CharField(max_length=100, blank=True, null=True)
    dr_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True, default='Pending')


    def save(self, *args, **kwargs):
        today = localdate()  # uses system local time

        if self.status == 'Cancelled':
            super().save(*args, **kwargs)
            return

        # Calculate total_days (clamp to 0, respect completion date)
        if self.date_started:
            end_date = self.completion_date if self.completion_date else today
            delta_days = (end_date - self.date_started).days
            self.total_days = max(0, delta_days)
        else:
            self.total_days = 0

        self.target_date_delayed = 0

        # Status logic
        if self.completion_date:
            self.status = 'Completed'

        elif self.target_date and self.target_date < today:
            self.status = 'Delayed'
            self.target_date_delayed = (today - self.target_date).days

        elif self.date_started and self.date_started <= today:
            self.status = 'Ongoing'

        else:
            self.status = 'Pending'

        # track adjusted target date
        if self.pk:
            # This is an update, not creation
            original = PurchaseOrder.objects.get(pk=self.pk)
            if original.target_date != self.target_date:
                self.target_date_status = "adjusted"

        super().save(*args, **kwargs)

    def update_totals(self):
        from .models import ManpowerDetail  # avoid circular import
        daily_logs = self.daily_work_statuses.all()

        manpower_total = 0
        work_hours_total = 0
        working_days_total = 0

        for log in daily_logs:
            # Get all manpower details for this log
            manpower_details = ManpowerDetail.objects.filter(dailyworkstatus=log)

            total_count = manpower_details.count()
            valid_count = manpower_details.filter(category__in=["Employee", "Both"]).count()

            if log.time_total is not None and total_count > 0:
                manpower_total += total_count
                working_days_total += 1
                work_hours_total += valid_count * log.time_total

        self.manpower_total = manpower_total
        self.working_days_total = working_days_total
        self.work_hours_total = work_hours_total
        self.save(update_fields=['manpower_total', 'working_days_total', 'work_hours_total'])


    def __str__(self):
        return f"{self.purchase_order}"
    
    def customer(self):
        return f"{self.customer_branch.customer_name} - {self.customer_branch.branch_name}"
    customer.short_description = 'Customer'


class DailyWorkStatus(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='daily_work_statuses')
    date = models.DateField(blank=True, null=True)
    manpower = models.ManyToManyField(ManpowerDetail, blank=True)
    time_total = models.PositiveIntegerField(blank=True, null=True)
    itinenary_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        manpower_list = ", ".join([m.name for m in self.manpower.all()])
        return f"{self.date} - {self.purchase_order.purchase_order} ({self.time_total} hrs)"

#signals


def update_purchase_order_manpower_type(purchase_order):
    from .models import ManpowerDetail  # avoid circular import

    manpower = ManpowerDetail.objects.filter(
        dailyworkstatus__purchase_order=purchase_order
    ).distinct()

    categories = set(m.category for m in manpower)

    if categories == {"Employee"}:
        purchase_order.manpower_type = "employee"
    elif categories == {"Contractor"}:
        purchase_order.manpower_type = "contractor"
    elif categories == {"Employee", "Contractor"}:
        purchase_order.manpower_type = "both"
    else:
        purchase_order.manpower_type = None

    purchase_order.save(update_fields=["manpower_type"])

@receiver(m2m_changed, sender=DailyWorkStatus.manpower.through)
def update_manpower_type_on_m2m_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        update_purchase_order_manpower_type(instance.purchase_order)

@receiver(post_save, sender=DailyWorkStatus)
def update_manpower_type_on_dws_save(sender, instance, **kwargs):
    update_purchase_order_manpower_type(instance.purchase_order)

@receiver(post_save, sender=DailyWorkStatus)
@receiver(post_delete, sender=DailyWorkStatus)
def update_po_totals_on_change(sender, instance, **kwargs):
    instance.purchase_order.update_totals()

@receiver(m2m_changed, sender=DailyWorkStatus.manpower.through)
def update_po_totals_on_m2m_change(sender, instance, **kwargs):
    instance.purchase_order.update_totals()