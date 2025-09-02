from rest_framework.routers import DefaultRouter
from .views import ReceiptViewSet

router = DefaultRouter()
router.register(r'', ReceiptViewSet, basename='receipt')

urlpatterns = router.urls
