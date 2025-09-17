# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Receipt
# from .utils import create_receipt_voucher

# @receiver(post_save, sender=Receipt)
# def create_voucher_on_receipt(sender, instance, created, **kwargs):
#     if created:
#         create_receipt_voucher(instance)

# receipts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Receipt
from .utils import create_receipt_voucher
from journals.models import JournalEntry


@receiver(post_save, sender=Receipt)
def create_or_update_voucher_on_receipt(sender, instance, created, **kwargs):
    """
    Create or update voucher whenever a receipt is saved.
    """
    if created:
        # New receipt → create a new voucher
        create_receipt_voucher(instance)
    else:
        # Edited receipt → update existing voucher
        if hasattr(instance, "journal_entry") and instance.journal_entry:
            # Delete old voucher lines
            instance.journal_entry.lines.all().delete()
            # Recreate voucher lines
            create_receipt_voucher(instance, journal=instance.journal_entry)
        else:
            # If no voucher exists (fallback), create new
            create_receipt_voucher(instance)


@receiver(post_delete, sender=Receipt)
def delete_voucher_on_receipt_delete(sender, instance, **kwargs):
    """
    Delete voucher when receipt is deleted.
    """
    if hasattr(instance, "journal_entry") and instance.journal_entry:
        instance.journal_entry.delete()
