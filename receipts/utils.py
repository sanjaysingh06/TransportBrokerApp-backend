from decimal import Decimal
from django.db import transaction
from accounts.models import Account
from journals.models import JournalEntry, JournalEntryLine

def create_receipt_voucher(receipt):
    """
    Create a voucher for the receipt with proper account mapping.
    """
    try:
        with transaction.atomic():
            # Linked accounts
            party_account = receipt.party_account
            transport_account = receipt.transport_account
            delivery_account = receipt.delivery_person

            # Fixed accounts from DB
            comm_account = Account.objects.get(name="Commission")         # id=9
            cartage_account = Account.objects.get(name="Cartage Account")  # id=29
            labour_account = Account.objects.get(name="Labour Expenses")   # id=11
            other_account = Account.objects.get(name="Other Charges")      # id=19

            # Create Journal Entry (Voucher)
            journal_entry = JournalEntry.objects.create(
                voucher_type="JV",
                date=receipt.date,
                narration=f"Receipt {receipt.receipt_no}"
            )

            # Debit: Party Account
            JournalEntryLine.objects.create(
                journal=journal_entry,
                account=party_account,
                debit=Decimal(receipt.total or 0),
                credit=Decimal("0.00"),
                remarks="Total receipt amount"
            )

            # Credit lines
            credit_lines = [
                (transport_account, receipt.freight, "Freight charges"),
                (comm_account, receipt.comm, "Commission charges"),
                (cartage_account, receipt.cartage, "Cartage charges"),
                (labour_account, receipt.labour, "Labour charges"),
                (other_account, receipt.other, "Other charges"),
                (delivery_account, receipt.delivery_charge, "Delivery charges"),
            ]

            for account, amount, remark in credit_lines:
                if account and amount and Decimal(amount) > 0:
                    JournalEntryLine.objects.create(
                        journal=journal_entry,
                        account=account,
                        debit=Decimal("0.00"),
                        credit=Decimal(amount),
                        remarks=remark
                    )

    except Exception as e:
        print(f"Error creating voucher for receipt {receipt.receipt_no}: {e}")
