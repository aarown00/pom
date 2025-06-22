from django.db import models

class CustomerDetail(models.Model):
    customer_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.customer_name} - {self.branch_name}"

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Delayed', 'Delayed'),
    ]

    REMARKS_CHOICES = [
        ('FOR BILLING', 'FOR BILLING'),
        ('FOR SIGNATURE', 'FOR SIGNATURE'),
    ]

    purchase_order = models.CharField(max_length=100)
    date_in_email = models.DateField()
    customer_branch = models.ForeignKey(CustomerDetail, on_delete=models.CASCADE)

    total_days = models.PositiveIntegerField()
    manpower_count = models.PositiveIntegerField()
    time_total = models.PositiveIntegerField()

    # Automatically calculate work hours
    @property
    def total_work_hour(self):
        return self.manpower_count * self.time_total

    description = models.TextField()
    remarks = models.CharField(max_length=20, choices=REMARKS_CHOICES)
    date_started = models.DateField()
    target_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.purchase_order}"
    
    def customer(self):
        return f"{self.customer_branch.customer_name} - {self.customer_branch.branch_name}"
    customer.short_description = 'Customer'
