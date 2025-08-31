from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Receipt
from .serializers import ReceiptSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all().order_by('-date')
    serializer_class = ReceiptSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    # ✅ FIXED: use related lookups
    search_fields = ['receipt_no', 'party_account__name', 'payment_type']
    ordering_fields = ['date', 'total']  # "total" exists, "amount" doesn't

    filterset_fields = {
        'date': ['gte', 'lte'],
        'payment_type': ['exact'],
        'party_account': ['exact'],
        'transport_account': ['exact'],
        'delivery_person': ['exact'],
    }
