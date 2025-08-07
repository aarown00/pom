from django.contrib import admin
from .models import CustomerDetail, PurchaseOrder, ManpowerDetail, DailyWorkStatus

# Inline for DailyWorkStatus
class DailyWorkStatusInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = DailyWorkStatus
    extra = 1  # number of empty forms to show
    filter_horizontal = ('manpower',)  # for better many-to-many UI

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'date_recorded',
    'purchase_order',
    'amount',
    'status',
    )
    readonly_fields = (
        'target_date_delayed',
        'total_days',
        'manpower_total',
        'work_hours_total',
        'working_days_total',
    )

    inlines = [DailyWorkStatusInline]  # attach DailyWorkStatus inline here


    class Media:
        css = {
            'all': ('css/admin.css',)
        }

@admin.register(ManpowerDetail)
class ManpowerDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'branch_name')

