from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import JournalEntry
from .serializers import JournalEntrySerializer


class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.prefetch_related('lines__account').all().order_by('-date', '-id')
    serializer_class = JournalEntrySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['voucher_no', 'narration', 'lines__account__code', 'lines__account__name']
    filterset_fields = {
        'date': ['gte', 'lte'],
        'voucher_no': ['exact'],
    }
