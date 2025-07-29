# monitoring/apps.py

from django.apps import AppConfig
from django.utils.timezone import localdate

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        from django.db.utils import OperationalError
        from django.core.cache import cache
        from monitoring.models import PurchaseOrder  # import your model here

        try:
            today = str(localdate())
            if cache.get('status_updated_on') == today:
                return  # already updated today

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

        except OperationalError:
            pass  # e.g., during migrate or startup issues
