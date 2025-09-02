from decimal import Decimal
from django.db import models
from django.utils import timezone
from accounts.models import Account  # ✅ import from accounts


class JournalEntry(models.Model):
    """Journal/Voucher header."""
    voucher_no = models.CharField(max_length=64, unique=True)
    date = models.DateField(default=timezone.now)
    narration = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.voucher_no} | {self.date}"


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
