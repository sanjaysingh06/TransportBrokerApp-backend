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
        # Import inside to avoid AppRegistryNotReady errors
        from .models import AccountType, Account

        try:
            # Ensure some system account types exist
            asset_type, _ = AccountType.objects.get_or_create(
                code="ASSET",
                defaults={"name": "Assets", "is_system": True}
            )
            liability_type, _ = AccountType.objects.get_or_create(
                code="LIAB",
                defaults={"name": "Liabilities", "is_system": True}
            )

            # Create predefined parent accounts if not exists
            receivable, _ = Account.objects.get_or_create(
                code="AR",
                defaults={
                    "name": "Accounts Receivable",
                    "account_type": asset_type,
                    "is_system": True,
                }
            )
            payable, _ = Account.objects.get_or_create(
                code="AP",
                defaults={
                    "name": "Accounts Payable",
                    "account_type": liability_type,
                    "is_system": True,
                }
            )

            # Sub-parents under receivable/payable
            Account.objects.get_or_create(
                code="PARTY",
                defaults={
                    "name": "Party Accounts",
                    "account_type": asset_type,
                    "parent": receivable,
                    "is_system": True,
                }
            )
            Account.objects.get_or_create(
                code="TRANSPORT",
                defaults={
                    "name": "Transport Accounts",
                    "account_type": liability_type,
                    "parent": payable,
                    "is_system": True,
                }
            )
        except (OperationalError, ProgrammingError):
            # Database might not be ready yet (e.g., during migrations)
            pass
