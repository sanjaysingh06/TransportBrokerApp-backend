# from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import AccountType, Account, JournalEntry
# from .serializers import (
#     AccountTypeSerializer,
#     AccountSerializer,
#     JournalEntrySerializer,
# )


# # ---------- Phase 1 ----------
# class AccountTypeViewSet(viewsets.ModelViewSet):
#     queryset = AccountType.objects.all().order_by('code')
#     serializer_class = AccountTypeSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['code', 'name']


# class AccountViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.select_related('account_type', 'parent').all().order_by('code')
#     serializer_class = AccountSerializer
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ['code', 'name']
#     filterset_fields = ['account_type', 'parent', 'is_active']


# # ---------- Phase 2 ----------
# class JournalEntryViewSet(viewsets.ModelViewSet):
#     queryset = JournalEntry.objects.prefetch_related('lines__account').all().order_by('-date', '-id')
#     serializer_class = JournalEntrySerializer
#     filter_backends = [filters.SearchFilter, DjangoFilterBackend]
#     search_fields = ['voucher_no', 'narration', 'lines__account__code', 'lines__account__name']
#     filterset_fields = {
#         'date': ['gte', 'lte'],
#         'voucher_no': ['exact'],
#     }



from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AccountType, Account
from .serializers import AccountTypeSerializer, AccountSerializer


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all().order_by('code')
    serializer_class = AccountTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name']


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('account_type', 'parent').all().order_by('code')
    serializer_class = AccountSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['code', 'name']
    filterset_fields = ['account_type', 'parent', 'is_active']
