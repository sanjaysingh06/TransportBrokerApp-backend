# from decimal import Decimal
# from django.db import models
# from django.utils import timezone
# from accounts.models import Account  # ✅ import from accounts


# class JournalEntry(models.Model):
#     """Journal/Voucher header."""
#     voucher_no = models.CharField(max_length=64, unique=True)
#     date = models.DateField(default=timezone.now)
#     narration = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-date', '-id']

#     def __str__(self):
#         return f"{self.voucher_no} | {self.date}"


# class JournalEntryLine(models.Model):
#     """Lines: exactly one of debit or credit must be > 0."""
#     journal = models.ForeignKey(
#         JournalEntry,
#         on_delete=models.CASCADE,
#         related_name='lines'
#     )
#     account = models.ForeignKey(
#         Account,
#         on_delete=models.PROTECT
#     )
#     debit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
#     credit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
#     remarks = models.CharField(max_length=255, blank=True)

#     class Meta:
#         ordering = ['id']
#         indexes = [
#             models.Index(fields=['account']),
#             models.Index(fields=['journal']),
#         ]

#     def __str__(self):
#         return f"{self.journal.voucher_no} - {self.account.code} ({self.debit}/{self.credit})"


from decimal import Decimal
from django.db import models
from django.utils import timezone
from accounts.models import Account


class JournalEntry(models.Model):
    """Journal/Voucher header."""
    voucher_no = models.CharField(max_length=64, unique=True, editable=False)
    date = models.DateField(default=timezone.now)
    narration = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.voucher_no} | {self.date}"

    def save(self, *args, **kwargs):
        if not self.voucher_no:  # generate only if new
            prefix = "JV"
            last_entry = JournalEntry.objects.filter(voucher_no__startswith=prefix).order_by('-id').first()
            
            if last_entry:
                last_number = int(last_entry.voucher_no.replace(f"{prefix}-", ""))
                new_number = last_number + 1
            else:
                new_number = 1

            # Always 5 digits with leading zeros
            self.voucher_no = f"{prefix}-{new_number:05d}"
        
        super().save(*args, **kwargs)


class JournalEntryLine(models.Model):
    """Lines: exactly one of debit or credit must be > 0."""
    journal = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )
    debit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    credit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['journal']),
        ]

    def __str__(self):
        return f"{self.journal.voucher_no} - {self.account.code} ({self.debit}/{self.credit})"
