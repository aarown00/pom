# monitoring/purchase_order_logic.py
from django.utils import timezone

def calculate_total_days(date_started, completion_date):
    if not date_started:
        return 0

    end_date = completion_date if completion_date else timezone.now().date()
    return max(0, (end_date - date_started).days)

def determine_status(date_started, completion_date, target_date, current_status):
    today = timezone.now().date()

    # Priority 0: Keep 'Cancelled' if set manually
    if current_status == 'Cancelled':
        return 'Cancelled', 0

    # Priority 1: Completed
    if completion_date:
        return 'Completed', 0

    # Priority 2: Delayed
    if target_date and target_date < today:
        delayed_days = (today - target_date).days
        return 'Delayed', delayed_days

    # Priority 3: Ongoing
    if date_started and date_started <= today:
        return 'Ongoing', 0

    # Priority 4: Pending
    return 'Pending', 0

def is_already_cancelled(instance):
    """Check if this instance is already marked Cancelled in DB (during update)"""
    if instance.pk:
        from .models import PurchaseOrder  # local import to avoid circular dependency
        old = PurchaseOrder.objects.get(pk=instance.pk)
        return old.status == 'Cancelled'
    return False
