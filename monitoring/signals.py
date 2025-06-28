# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from .models import CustomerDetail, PurchaseOrder, ManpowerDetail

# @receiver(m2m_changed, sender=PurchaseOrder.manpower.through)
# def update_manpower_total(sender, instance, action, **kwargs):
#     if action in ['post_add', 'post_remove', 'post_clear']:
#         instance.manpower_total = instance.manpower.count()
#         instance.save(update_fields=['manpower_total'])
