from decimal import Decimal
from django.db import transaction
from accounts.models import Account, AccountType, JournalEntry, JournalEntryLine

def create_receipt_voucher(receipt):
    """
    Create a voucher for each receipt with separate accounts for freight, commission, cartage, labour, other,
    party, transport, and delivery accounts. Auto-create accounts if missing.
    """
    try:
        # Wrap all operations in a transaction
        with transaction.atomic():
            # Fetch or create account types
            party_type = AccountType.objects.get(id=3)       # Party
            transport_type = AccountType.objects.get(id=4)   # Transport
            delivery_type = AccountType.objects.get(id=5)    # Delivery
            expense_type = AccountType.objects.get(id=6)     # Expense accounts (Comm, Cartage, Labour, Other)

            # Fetch or create dynamic accounts
            party_account = Account.objects.get_or_create(name=receipt.party_name, account_type=party_type)[0]
            transport_account = Account.objects.get_or_create(name=receipt.transport_name, account_type=transport_type)[0]
            delivery_account = Account.objects.get_or_create(name=receipt.delivery_person, account_type=delivery_type)[0]

            # Fetch or create fixed expense accounts
            comm_account = Account.objects.get_or_create(name="Comm Account", account_type=expense_type)[0]
            cartage_account = Account.objects.get_or_create(name="Cartage Account", account_type=expense_type)[0]
            labour_account = Account.objects.get_or_create(name="Labour Account", account_type=expense_type)[0]
            other_account = Account.objects.get_or_create(name="Other Account", account_type=expense_type)[0]

            # Create Journal/Voucher header
            journal_entry = JournalEntry.objects.create(
                voucher_no=f"RCPT-{receipt.receipt_no}",
                date=receipt.date,
                narration=f"Receipt {receipt.receipt_no} from {receipt.party_name}"
            )

            # Party debit
            JournalEntryLine.objects.create(
                journal=journal_entry,
                account=party_account,
                debit=Decimal(receipt.total or 0),
                credit=Decimal('0.00'),
                remarks="Total receipt amount"
            )

            # List of credit accounts with amounts
            credit_lines = [
                (transport_account, receipt.freight, "Freight charges"),
                (comm_account, receipt.comm, "Commission charges"),
                (cartage_account, receipt.cartage, "Cartage charges"),
                (labour_account, receipt.labour, "Labour charges"),
                (other_account, receipt.other, "Other charges"),
                (delivery_account, receipt.delivery_charge, "Delivery charges")
            ]

            # Create credit entries
            for account, amount, remark in credit_lines:
                if amount and amount > 0:
                    JournalEntryLine.objects.create(
                        journal=journal_entry,
                        account=account,
                        debit=Decimal('0.00'),
                        credit=Decimal(amount),
                        remarks=remark
                    )

    except Exception as e:
        print(f"Error creating voucher for receipt {receipt.receipt_no}: {e}")
