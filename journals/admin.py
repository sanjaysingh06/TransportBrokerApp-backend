from django.contrib import admin
from .models import JournalEntry, JournalEntryLine


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 0


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('voucher_no', 'date', 'narration', 'created_at')
    search_fields = ('voucher_no', 'narration')
    inlines = [JournalEntryLineInline]
