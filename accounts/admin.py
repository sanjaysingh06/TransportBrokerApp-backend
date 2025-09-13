
# from django.contrib import admin
# from .models import AccountType, Account


# @admin.register(AccountType)
# class AccountTypeAdmin(admin.ModelAdmin):
#     list_display = ('code', 'name')
#     search_fields = ('code', 'name')


# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('code', 'name', 'account_type', 'parent', 'is_active', 'opening_balance')
#     list_filter = ('account_type', 'is_active')
#     search_fields = ('code', 'name')
#     raw_id_fields = ('parent',)


from django.contrib import admin
from .models import AccountType, Account


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_system')
    list_filter = ('is_system',)
    search_fields = ('code', 'name')
    readonly_fields = ('is_system',)  # prevent editing system flag directly


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'account_type', 'parent',
        'is_active', 'opening_balance', 'is_system'
    )
    list_filter = ('account_type', 'is_active', 'is_system')
    search_fields = ('code', 'name')
    raw_id_fields = ('parent',)
    readonly_fields = ('is_system',)  # prevent accidental changes
