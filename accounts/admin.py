# from django.contrib import admin
# from .models import AccountType, Account, JournalEntry, JournalEntryLine


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


# class JournalEntryLineInline(admin.TabularInline):
#     model = JournalEntryLine
#     extra = 0


# @admin.register(JournalEntry)
# class JournalEntryAdmin(admin.ModelAdmin):
#     list_display = ('voucher_no', 'date', 'narration', 'created_at')
#     search_fields = ('voucher_no', 'narration')
#     inlines = [JournalEntryLineInline]

from django.contrib import admin
from .models import AccountType, Account


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'account_type', 'parent', 'is_active', 'opening_balance')
    list_filter = ('account_type', 'is_active')
    search_fields = ('code', 'name')
    raw_id_fields = ('parent',)
