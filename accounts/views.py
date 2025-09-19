from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AccountType, Account
from .serializers import AccountTypeSerializer, AccountSerializer


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all().order_by('code')
    serializer_class = AccountTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {"error": "System-defined account types cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {"error": "System-defined account types cannot be modified."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('account_type', 'parent').all().order_by('code')
    serializer_class = AccountSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['code', 'name']
    filterset_fields = ['account_type', 'parent', 'is_active']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {"error": "System-defined accounts cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_system:
            return Response(
                {"error": "System-defined accounts cannot be modified."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)
