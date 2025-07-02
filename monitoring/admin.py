from django.contrib import admin
from .models import CustomerDetail, PurchaseOrder, ManpowerDetail

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'purchase_order',
        'customer',
        'classification',
        'description',
        'manpower_total',
        'date_recorded',
        'purchase_order_received',
        'date_started',
        'target_date',
        'completion_date',
        'coc_number',
        'service_report_number',
        'dr_number',
        'invoice_number',
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
    list_display = ('name', 'category')

@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'branch_name')

