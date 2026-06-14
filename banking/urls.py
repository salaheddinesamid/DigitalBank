from rest_framework.routers import DefaultRouter
from .views.transactions_view import AccountTransactionViewSet
from .views.account_view import AccountDetailViewSet

router = DefaultRouter()

router.register(r'accounts', AccountDetailViewSet, basename='accounts')
router.register(r'transactions', AccountTransactionViewSet, basename='transactions')

urlpatterns = router.urls
