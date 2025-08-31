from django.urls import path
from .views import LedgerReportView, TrialBalanceReportView

urlpatterns = [
    path("ledger/", LedgerReportView.as_view(), name="ledger-report"),
    path("trial-balance/", TrialBalanceReportView.as_view(), name="trial-balance-report"),
]
