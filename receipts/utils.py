# receipts/utils.py
from decimal import Decimal
from django.db import transaction
from accounts.models import Account
from journals.models import JournalEntry, JournalEntryLine
import logging

logger = logging.getLogger(__name__)

def create_receipt_voucher(receipt, journal=None):
    """
    Create or update a voucher for the receipt with proper account mapping.
    If `journal` is provided → update existing journal entry.
    Otherwise → create a new one.

    This function logs errors and ensures that missing accounts are reported.
    """
    try:
        with transaction.atomic():
            # Linked accounts
            party_account = receipt.party_account
            transport_account = receipt.transport_account
            delivery_account = receipt.delivery_person

            if not party_account:
                raise ValueError(f"Party account missing for receipt {receipt.receipt_no}")

            # Fixed accounts from DB with safe get_or_create
            comm_account, _ = Account.objects.get_or_create(name="Commission")
            cartage_account, _ = Account.objects.get_or_create(name="Cartage")
            labour_account, _ = Account.objects.get_or_create(name="Labour Expenses")
            other_account, _ = Account.objects.get_or_create(name="Other Charges")

            # Create new JournalEntry if not passed
            if not journal:
                journal = JournalEntry.objects.create(
                    voucher_type="JV",
                    date=receipt.date,
                    narration=f"Receipt {receipt.receipt_no}"
                )

            # Clear existing lines before recreating
            journal.lines.all().delete()

            # Debit: Party Account
            JournalEntryLine.objects.create(
                journal=journal,
                account=party_account,
                debit=Decimal(receipt.total or 0),
                credit=Decimal("0.00"),
                remarks="Total receipt amount"
            )

            # Credit lines mapping
            credit_lines = [
                (transport_account, receipt.freight, "Freight charges"),
                (comm_account, receipt.comm, "Commission charges"),
                (cartage_account, receipt.cartage, "Cartage charges"),
                (labour_account, receipt.labour, "Labour charges"),
                (other_account, receipt.other, "Other charges"),
                (delivery_account, receipt.delivery_charge, "Delivery charges"),
            ]

            # Create credit entries only if account exists and amount > 0
            for account, amount, remark in credit_lines:
                if account and amount and Decimal(amount) > 0:
                    JournalEntryLine.objects.create(
                        journal=journal,
                        account=account,
                        debit=Decimal("0.00"),
                        credit=Decimal(amount),
                        remarks=remark
                    )

            # Save reference of voucher to receipt
            if not receipt.journal_entry:
                receipt.journal_entry = journal
                receipt.save(update_fields=["journal_entry"])

            return journal

    except Exception as e:
        # Log full stack trace
        logger.exception(f"Error creating voucher for receipt {receipt.receipt_no}")
        # Re-raise the exception in development so you see it immediately
        raise
