from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Receipt
from .utils import create_receipt_voucher

@receiver(post_save, sender=Receipt)
def create_voucher_on_receipt(sender, instance, created, **kwargs):
    if created:
        create_receipt_voucher(instance)
