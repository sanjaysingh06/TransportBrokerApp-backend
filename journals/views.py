from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import JournalEntry
from .serializers import JournalEntrySerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.prefetch_related('lines__account').all().order_by('-date', '-id')
    serializer_class = JournalEntrySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['voucher_no', 'voucher_type','narration', 'lines__account__code', 'lines__account__name']
    filterset_fields = {
        'date': ['gte', 'lte'],
        'voucher_no': ['exact'],
        'voucher_type': ['exact'],
    }

    @action(detail=False, methods=["get"], url_path="next-voucher")
    def next_voucher(self, request):
        voucher_type = request.query_params.get("type", "JV")
        prefix_map = {
            "Receipt": "RV",
            "Payment": "PV",
            "Income": "JV",
            "Expense": "JV",
        }
        prefix = prefix_map.get(voucher_type, "JV")

        last_entry = JournalEntry.objects.filter(voucher_no__startswith=prefix).order_by("-id").first()
        if last_entry:
            try:
                last_number = int(last_entry.voucher_no.replace(f"{prefix}-", ""))
            except ValueError:
                last_number = 0
            new_number = last_number + 1
        else:
            new_number = 1

        next_voucher_no = f"{prefix}-{new_number:05d}"
        return Response({"next_voucher_no": next_voucher_no})
