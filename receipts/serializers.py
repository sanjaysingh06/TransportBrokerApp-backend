from rest_framework import serializers
from .models import Receipt
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name"]


class ReceiptSerializer(serializers.ModelSerializer):
    # Read-only nested representation
    transport_account = AccountSerializer(read_only=True)
    party_account = AccountSerializer(read_only=True)
    delivery_person = AccountSerializer(read_only=True)

    # Write-only fields for creating/updating (accepts IDs)
    transport_account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source="transport_account",
        write_only=True,
        required=False,  # <-- make optional
        allow_null=True
    )
    party_account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source="party_account",
        write_only=True,
        required=False,
        allow_null=True
    )
    delivery_person_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source="delivery_person",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Receipt
        fields = "__all__"
