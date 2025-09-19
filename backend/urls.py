# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # existing apps (unchanged)
    path('api/', include('accounts.urls')),
    path('api/journal-entries/', include('journals.urls')),
    path('api/receipts/', include('receipts.urls')),
    path('api/reports/', include('reports.urls')),

    # optional session login (browsable API)
    path('api/auth/', include('rest_framework.urls')),

    # NEW: JWT auth endpoints (grouped)
    path('api/auth/', include('users.urls')),   # -> /api/auth/token/, /api/auth/me/, etc.
]
