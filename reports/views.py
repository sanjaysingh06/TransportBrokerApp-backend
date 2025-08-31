from decimal import Decimal
from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Account, JournalEntry, JournalEntryLine  # adjust if reports in diff app

class LedgerReportView(APIView):
    """
    GET /api/reports/ledger/?account_id=1&start_date=2025-01-01&end_date=2025-01-31
    """

    def get(self, request):
        account_id = request.GET.get("account_id")
        if not account_id:
            return Response({"detail": "account_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        include_opening = request.GET.get("include_opening", "true").lower() in ("1", "true", "yes")
        search = request.GET.get("search")
        min_amount = request.GET.get("min_amount")
        max_amount = request.GET.get("max_amount")

        # validate account
        try:
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        # base queryset of lines
        lines = JournalEntryLine.objects.select_related("journal").filter(account_id=account_id)

        if start_date:
            lines = lines.filter(journal__date__gte=start_date)
        if end_date:
            lines = lines.filter(journal__date__lte=end_date)
        if search:
            lines = lines.filter(
                Q(journal__voucher_no__icontains=search) |
                Q(journal__narration__icontains=search) |
                Q(remarks__icontains=search)
            )
        if min_amount:
            lines = lines.filter(Q(debit__gte=min_amount) | Q(credit__gte=min_amount))
        if max_amount:
            lines = lines.filter(Q(debit__lte=max_amount) | Q(credit__lte=max_amount))

        # opening balance = before start_date
        opening_balance = Decimal("0.00")
        if include_opening and start_date:
            ob = (JournalEntryLine.objects
                  .filter(account_id=account_id, journal__date__lt=start_date)
                  .aggregate(
                      debit=Coalesce(Sum("debit"), Value("0.00", output_field=DecimalField())),
                      credit=Coalesce(Sum("credit"), Value("0.00", output_field=DecimalField()))
                  ))
            opening_balance = ob["debit"] - ob["credit"]

        totals = lines.aggregate(
            debit=Coalesce(Sum("debit"), Value("0.00", output_field=DecimalField())),
            credit=Coalesce(Sum("credit"), Value("0.00", output_field=DecimalField())),
        )
        total_debit = totals["debit"]
        total_credit = totals["credit"]

        # build ledger rows
        transactions = []
        running = opening_balance

        for line in lines.order_by("journal__date", "journal_id", "id"):
            debit = line.debit or Decimal("0.00")
            credit = line.credit or Decimal("0.00")
            running = running + debit - credit
            transactions.append({
                "date": line.journal.date,
                "voucher_no": line.journal.voucher_no,
                "description": line.journal.narration or line.remarks,
                "debit": debit,
                "credit": credit,
                "balance": running,
                "journal_id": line.journal_id,
                "line_id": line.id
            })

        closing_balance = opening_balance + total_debit - total_credit

        return Response({
            "account": {"id": account.id, "name": account.name, "code": account.code},
            "start_date": start_date,
            "end_date": end_date,
            "opening_balance": opening_balance,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "closing_balance": closing_balance,
            "transactions": transactions
        })


class TrialBalanceReportView(APIView):
    """
    GET /api/reports/trial-balance/?start_date=2025-01-01&end_date=2025-01-31
    """

    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        account_type = request.GET.get("account_type")
        search = request.GET.get("search")

        lines = JournalEntryLine.objects.select_related("journal", "account")

        if start_date:
            lines = lines.filter(journal__date__gte=start_date)
        if end_date:
            lines = lines.filter(journal__date__lte=end_date)
        if account_type:
            lines = lines.filter(account__account_type_id=account_type)
        if search:
            lines = lines.filter(account__name__icontains=search)

        by_account = (lines.values("account_id", "account__name", "account__code")
                      .annotate(
                          debit_total=Coalesce(Sum("debit"), Value("0.00", output_field=DecimalField())),
                          credit_total=Coalesce(Sum("credit"), Value("0.00", output_field=DecimalField())),
                      )
                      .order_by("account__code"))

        accounts = []
        total_debit = Decimal("0.00")
        total_credit = Decimal("0.00")

        for row in by_account:
            debit_total = row["debit_total"]
            credit_total = row["credit_total"]
            closing_balance = debit_total - credit_total

            accounts.append({
                "account_id": row["account_id"],
                "account_code": row["account__code"],
                "account_name": row["account__name"],
                "debit_total": debit_total,
                "credit_total": credit_total,
                "closing_balance": closing_balance
            })
            total_debit += debit_total
            total_credit += credit_total

        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "accounts": accounts,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "is_balanced": (total_debit == total_credit)
        })