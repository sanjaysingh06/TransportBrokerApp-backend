from decimal import Decimal
from django.db import transaction
from accounts.models import Account, AccountType
from journals.models import JournalEntry, JournalEntryLine


def create_receipt_voucher(receipt):
    """
    Create a voucher for each receipt with separate accounts for freight, commission, cartage, labour, other,
    party, transport, and delivery accounts.
    All vouchers created here will fall under Journal Vouchers (JV series).
    """
    try:
        with transaction.atomic():
            # Correct account types from DB
            income_type = AccountType.objects.get(id=5)   # Comm, Cartage, Other (Income)
            expense_type = AccountType.objects.get(id=6)  # Labour (Expense)

            # Use linked accounts directly from receipt
            party_account = receipt.party_account
            transport_account = receipt.transport_account
            delivery_account = receipt.delivery_person

            # Fixed accounts with explicit codes
            comm_account, _ = Account.objects.get_or_create(
                name="Comm Account", account_type=income_type,
                defaults={"code": "1500"}
            )
            cartage_account, _ = Account.objects.get_or_create(
                name="Cartage Account", account_type=income_type,
                defaults={"code": "1501"}
            )
            labour_account, _ = Account.objects.get_or_create(
                name="Labour Account", account_type=expense_type,
                defaults={"code": "1502"}
            )
            other_account, _ = Account.objects.get_or_create(
                name="Other Account", account_type=income_type,
                defaults={"code": "1503"}
            )

            # Journal Entry (Voucher Header) → don’t set voucher_no, let auto JV series generate
            journal_entry = JournalEntry.objects.create(
                voucher_type="JV",  # explicitly Journal Voucher
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

            # Credit Lines
            credit_lines = [
                (transport_account, receipt.freight, "Freight charges"),
                (comm_account, receipt.comm, "Commission charges"),
                (cartage_account, receipt.cartage, "Cartage charges"),
                (labour_account, receipt.labour, "Labour charges"),
                (other_account, receipt.other, "Other charges"),
                (delivery_account, receipt.delivery_charge, "Delivery charges"),
            ]

            for account, amount, remark in credit_lines:
                if amount and Decimal(amount) > 0:
                    JournalEntryLine.objects.create(
                        journal=journal_entry,
                        account=account,
                        debit=Decimal("0.00"),
                        credit=Decimal(amount),
                        remarks=remark
                    )

    except Exception as e:
        print(f"Error creating voucher for receipt {receipt.receipt_no}: {e}")
