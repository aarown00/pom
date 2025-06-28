from django.contrib import admin
from .models import CustomerDetail, PurchaseOrder, ManpowerDetail

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date_recorded',
        'purchase_order',
        'customer', 
        'date_in_email',
        'target_date',
        'item_model',
        'description',
        'service_report',
        'total_days',
        'manpower_total',
        'time_total',
        'total_work_hour_display',
        'date_started',
        'completion_date',
        'completion_code',
        'delivery_code',
        'status',
    )

    filter_horizontal = ('manpower',)

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def total_work_hour_display(self, obj):
        return obj.total_work_hour
    total_work_hour_display.short_description = 'Total Work Hour'

@admin.register(ManpowerDetail)
class ManpowerDetailAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'branch_name')

