# from django.db import models
# from decimal import Decimal

# class Receipt(models.Model):
#     receipt_no = models.CharField(max_length=50, unique=True)
#     date = models.DateField()
#     transport_name = models.CharField(max_length=255, null=True, blank=True)  # transport account
#     party_name = models.CharField(max_length=255, null=True, blank=True)      # party account
#     gr_no = models.CharField(max_length=50, blank=True, null=True)
#     container = models.CharField(max_length=100, blank=True, null=True)
#     pkgs = models.PositiveIntegerField(default=0)
#     weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     freight = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     comm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     pkg_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     cartage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     labour = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     remark = models.TextField(blank=True, null=True)
#     delivery_date = models.DateField(blank=True, null=True)
#     delivery_person = models.CharField(max_length=255, blank=True, null=True)  # delivery account
#     delivery_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     delivery_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     payment_type = models.CharField(
#         max_length=20,
#         choices=[('cash', 'Cash'), ('bank', 'Bank'), ('upi', 'UPI')],
#         null=True,
#         blank=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         # Auto-calculate total
#         self.total = (
#             Decimal(self.freight or 0) +
#             Decimal(self.comm or 0) +
#             Decimal(self.cartage or 0) +
#             Decimal(self.labour or 0) +
#             Decimal(self.other or 0)
#         )
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.receipt_no} - {self.party_name}"



from django.db import models
from decimal import Decimal
from accounts.models import Account  # import Account model properly

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=50, unique=True)
    date = models.DateField()

    # ✅ Use ForeignKeys instead of CharField
    transport_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, null=True, blank=True, related_name="receipts_as_transport"
    )
    party_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, null=True, blank=True, related_name="receipts_as_party"
    )
    delivery_person = models.ForeignKey(
        Account, on_delete=models.PROTECT, null=True, blank=True, related_name="receipts_as_delivery"
    )

    gr_no = models.CharField(max_length=50, blank=True, null=True)
    container = models.CharField(max_length=100, blank=True, null=True)
    pkgs = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    freight = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    comm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pkg_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cartage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    labour = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remark = models.TextField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_type = models.CharField(
        max_length=20,
        choices=[('cash', 'Cash'), ('bank', 'Bank'), ('upi', 'UPI')],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total
        self.total = (
            Decimal(self.freight or 0) +
            Decimal(self.comm or 0) +
            Decimal(self.cartage or 0) +
            Decimal(self.labour or 0) +
            Decimal(self.other or 0)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_no} - {self.party_account.name if self.party_account else 'No Party'}"
