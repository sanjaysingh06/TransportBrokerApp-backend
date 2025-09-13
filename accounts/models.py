# from decimal import Decimal
# from django.db import models


# class AccountType(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=20, unique=True)

#     class Meta:
#         ordering = ['code']

#     def __str__(self):
#         return f"{self.code} - {self.name}"


# class Account(models.Model):
#     """
#     Chart of Accounts node. Supports hierarchy via parent.
#     Use opening_balance only for initialization; actual balances come from journals.
#     """
#     account_type = models.ForeignKey(
#         AccountType,
#         on_delete=models.PROTECT,
#         related_name='accounts'
#     )
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=40, unique=True)
#     parent = models.ForeignKey(
#         'self',
#         null=True, blank=True,
#         on_delete=models.CASCADE,
#         related_name='children'
#     )
#     is_active = models.BooleanField(default=True)
#     opening_balance = models.DecimalField(
#         max_digits=18, decimal_places=2,
#         default=Decimal('0.00')
#     )

#     class Meta:
#         ordering = ['code']
#         indexes = [
#             models.Index(fields=['code']),
#             models.Index(fields=['account_type']),
#         ]

#     def __str__(self):
#         return f"{self.code} - {self.name}"


from decimal import Decimal
from django.db import models


class AccountType(models.Model):
    """
    Broad classification (Asset, Liability, Income, Expense, Equity).
    Defines the natural balance side (Debit or Credit).
    """
    BALANCE_CHOICES = [
        ('D', 'Debit'),
        ('C', 'Credit'),
    ]

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    normal_balance = models.CharField(
        max_length=1,
        choices=BALANCE_CHOICES,
        help_text="Normal balance side for this account type",
        default='D'
    )
    is_system = models.BooleanField(
        default=False,
        help_text="True if system-defined and should not be deleted"
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Account(models.Model):
    """
    Chart of Accounts with hierarchy.
    Top-level accounts can be system-defined (e.g., Accounts Receivable).
    Users create sub-accounts under these (e.g., Party A).
    """
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.PROTECT,
        related_name='accounts'
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=40, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(
        default=False,
        help_text="True if system-defined and should not be deleted"
    )
    opening_balance = models.DecimalField(
        max_digits=18, decimal_places=2,
        default=Decimal('0.00')
    )

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['account_type']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def full_path(self):
        """Return hierarchical path like: Asset → Accounts Receivable → Party A"""
        parts = []
        account = self
        while account:
            parts.append(account.name)
            account = account.parent
        return " → ".join(reversed(parts))
