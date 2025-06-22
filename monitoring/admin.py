from django.contrib import admin
from .models import CustomerDetail, PurchaseOrder

@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'branch_name')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'purchase_order',
        'date_in_email',
        'customer',  # uses the method above
        'total_days',
        'manpower_count',
        'time_total',
        'total_work_hour_display',
        'description',
        'remarks',
        'date_started',
        'target_date',
        'completion_date',
        'status',
    )

    def total_work_hour_display(self, obj):
        return obj.total_work_hour
    total_work_hour_display.short_description = 'Total Work Hour'