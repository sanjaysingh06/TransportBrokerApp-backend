# from django.apps import AppConfig


# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'


from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Create system AccountTypes and Accounts if they don't already exist.
        This runs once on app startup.
        """
        from .models import AccountType, Account

        try:
            # -------- Account Types --------
            asset_type, _ = AccountType.objects.get_or_create(
                code="ASSET",
                defaults={"name": "Assets", "normal_balance": "D", "is_system": True}
            )

            liability_type, _ = AccountType.objects.get_or_create(
                code="LIAB",
                defaults={"name": "Liabilities", "normal_balance": "C", "is_system": True}
            )

            income_type, _ = AccountType.objects.get_or_create(
                code="INC",
                defaults={"name": "Income", "normal_balance": "C", "is_system": True}
            )

            expense_type, _ = AccountType.objects.get_or_create(
                code="EXP",
                defaults={"name": "Expense", "normal_balance": "D", "is_system": True}
            )

            # -------- System Accounts --------
            # Assets
            ar_account, _ = Account.objects.get_or_create(
                code="2000",
                defaults={
                    "name": "Accounts Receivable",
                    "account_type": asset_type,
                    "is_system": True
                }
            )

            cash_account, _ = Account.objects.get_or_create(
                code="1",
                defaults={
                    "name": "Cash In Hand",
                    "account_type": asset_type,
                    "is_system": True
                }
            )

            bank_account, _ = Account.objects.get_or_create(
                code="2",
                defaults={
                    "name": "Bank",
                    "account_type": asset_type,
                    "is_system": True
                }
            )

            # Sub-account under Accounts Receivable
            party_accounts, _ = Account.objects.get_or_create(
                code="2100",
                defaults={
                    "name": "Party Accounts",
                    "account_type": asset_type,
                    "parent": ar_account,
                    "is_system": True
                }
            )

            # Users can create Party A, Party B under party_accounts
            # Example system party
            Account.objects.get_or_create(
                code="2101",
                defaults={
                    "name": "Party A",
                    "account_type": asset_type,
                    "parent": party_accounts,
                    "is_system": True
                }
            )

            # Liabilities
            ap_account, _ = Account.objects.get_or_create(
                code="1001",
                defaults={
                    "name": "Accounts Payable",
                    "account_type": liability_type,
                    "is_system": True
                }
            )

            transport_accounts, _ = Account.objects.get_or_create(
                code="1100",
                defaults={
                    "name": "Transport Accounts",
                    "account_type": liability_type,
                    "parent": ap_account,
                    "is_system": True
                }
            )

            Account.objects.get_or_create(
                code="1101",
                defaults={
                    "name": "Transport X",
                    "account_type": liability_type,
                    "parent": transport_accounts,
                    "is_system": True
                }
            )

            # Income
            Account.objects.get_or_create(
                code="501",
                defaults={
                    "name": "Commission",
                    "account_type": income_type,
                    "is_system": True
                }
            )

            Account.objects.get_or_create(
                code="502",
                defaults={
                    "name": "Other Income",
                    "account_type": income_type,
                    "is_system": True
                }
            )

            # Expense
            Account.objects.get_or_create(
                code="601",
                defaults={
                    "name": "Labour Expenses",
                    "account_type": expense_type,
                    "is_system": True
                }
            )

        except (OperationalError, ProgrammingError):
            # Database not ready yet (during migrations)
            pass
