# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from receipts.views import ReceiptViewSet
# from accounts.views import AccountTypeViewSet, AccountViewSet, JournalEntryViewSet


# router = DefaultRouter()
# router.register(r'receipts', ReceiptViewSet)

# router.register(r'account-types', AccountTypeViewSet, basename='accounttype')
# router.register(r'accounts', AccountViewSet, basename='account')
# router.register(r'journal-entries', JournalEntryViewSet, basename='journalentry')

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/auth/', include('rest_framework.urls')),
#     path("api/reports/", include("reports.urls")),
    
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('accounts.urls')),
    path('api/journal-entries/', include('journals.urls')),
    path('api/receipts/', include('receipts.urls')),
    path('api/reports/', include('reports.urls')),

    # Browsable API login/logout
    path('api/auth/', include('rest_framework.urls')),
]
