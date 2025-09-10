from django.contrib import admin
from .models import JournalEntry, JournalEntryLine


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 0


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'voucher_type', 'date', 'narration', 'created_at')  # 👈 added voucher_type
    list_filter = ('voucher_type', 'date')  # 👈 filter by type and date
    search_fields = ('voucher_no', 'narration')
    inlines = [JournalEntryLineInline]
