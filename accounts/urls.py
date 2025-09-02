from rest_framework.routers import DefaultRouter
from .views import AccountTypeViewSet, AccountViewSet

router = DefaultRouter()
router.register(r'account-types', AccountTypeViewSet, basename='accounttype')
router.register(r'accounts', AccountViewSet, basename='account')

urlpatterns = router.urls
