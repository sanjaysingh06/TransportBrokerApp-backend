from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from .models import JournalEntry, JournalEntryLine


class JournalEntryLineSerializer(serializers.ModelSerializer):
    account_code = serializers.CharField(source='account.code', read_only=True)
    account_name = serializers.CharField(source='account.name', read_only=True)

    class Meta:
        model = JournalEntryLine
        fields = ['id', 'account', 'account_code', 'account_name', 'debit', 'credit', 'remarks']


class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True)

    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'voucher_type',   # 👈 new field
            'voucher_no',
            'date',
            'narration',
            'lines',
            'created_at'
        ]
        read_only_fields = ['created_at', 'voucher_no']

    def validate(self, data):
        lines = data.get('lines', [])
        if not lines or len(lines) < 2:
            raise serializers.ValidationError("Journal entry must have at least two lines.")

        total_debit = Decimal('0.00')
        total_credit = Decimal('0.00')

        for i, l in enumerate(lines, start=1):
            debit = Decimal(l.get('debit', 0) or 0)
            credit = Decimal(l.get('credit', 0) or 0)

            if debit < 0 or credit < 0:
                raise serializers.ValidationError(f"Line {i}: Debit/Credit cannot be negative.")
            if debit == 0 and credit == 0:
                raise serializers.ValidationError(f"Line {i}: Either debit or credit must be > 0.")
            if debit > 0 and credit > 0:
                raise serializers.ValidationError(f"Line {i}: Both debit and credit cannot be > 0.")

            total_debit += debit
            total_credit += credit

        if total_debit != total_credit:
            raise serializers.ValidationError({
                'non_field_errors': [
                    f"Entry not balanced: total_debit={total_debit} total_credit={total_credit}"
                ]
            })
        return data

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        with transaction.atomic():
            # voucher_type will either come from validated_data (if provided)
            # or fallback to model default ("JV")
            journal = JournalEntry.objects.create(**validated_data)
            for ld in lines_data:
                JournalEntryLine.objects.create(journal=journal, **ld)
        return journal

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)

        with transaction.atomic():
            # Update main journal entry fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Handle nested lines update
            if lines_data is not None:
                # Get existing lines
                existing_lines = {line.id: line for line in instance.lines.all()}
                
                # Update or create lines
                for line_data in lines_data:
                    line_id = line_data.get('id', None)
                    
                    if line_id and line_id in existing_lines:
                        # Update existing line
                        line = existing_lines[line_id]
                        for attr, value in line_data.items():
                            setattr(line, attr, value)
                        line.save()
                        del existing_lines[line_id]
                    else:
                        # Create new line
                        JournalEntryLine.objects.create(journal=instance, **line_data)
                
                # Delete lines that weren't included in the update
                for line in existing_lines.values():
                    line.delete()

        return instance