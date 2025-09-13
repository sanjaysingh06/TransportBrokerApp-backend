# from rest_framework import serializers
# from .models import AccountType, Account


# class AccountTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountType
#         fields = ['id', 'name', 'code']


# class AccountSerializer(serializers.ModelSerializer):
#     parent_name = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Account
#         fields = [
#             'id', 'account_type', 'name', 'code',
#             'parent', 'parent_name', 'is_active', 'opening_balance'
#         ]

#     def get_parent_name(self, obj):
#         return str(obj.parent) if obj.parent else None


from rest_framework import serializers
from .models import AccountType, Account


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = [
            'id',
            'name',
            'code',
            'normal_balance',  # NEW: lets frontend know if type is Debit or Credit by nature
            'is_system',       # NEW: protects system-defined types
        ]


class AccountSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField(read_only=True)
    full_path = serializers.ReadOnlyField()  # NEW: shows full hierarchy path

    class Meta:
        model = Account
        fields = [
            'id',
            'account_type',
            'name',
            'code',
            'parent',
            'parent_name',
            'is_active',
            'is_system',        # NEW: protects system-defined accounts
            'opening_balance',
            'full_path',        # NEW: helps display hierarchy like "Asset → Accounts Receivable → Party A"
        ]

    def get_parent_name(self, obj):
        return str(obj.parent) if obj.parent else None
