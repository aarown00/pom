import threading
import time
from django.apps import AppConfig
from django.core.cache import cache
from django.utils.timezone import localdate

def delayed_status_update():
    time.sleep(10)  # Delay before running logic

    from django.db.utils import OperationalError
    from monitoring.models import PurchaseOrder

    try:
        today = str(localdate())
        if cache.get('status_updated_on') == today:
            return

        print("Fetching purchase orders...")
        pos = PurchaseOrder.objects.exclude(status='Cancelled')
        for po in pos:
            original_status = po.status

            if po.completion_date:
                po.status = 'Completed'
            elif po.target_date and po.target_date < localdate():
                po.status = 'Delayed'
                po.target_date_delayed = (localdate() - po.target_date).days
            elif po.date_started and po.date_started <= localdate():
                po.status = 'Ongoing'
            else:
                po.status = 'Pending'

            if po.status != original_status:
                po.save()
                print(f"Updated PO {po.id}: {original_status} → {po.status}")

        cache.set('status_updated_on', today)
        print("Finished updating status.")

    except OperationalError as e:
        print("OperationalError: Likely during migrations or DB not ready")
    except Exception as e:
        print(f"Unexpected error: {e}")

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        threading.Thread(target=delayed_status_update).start()
