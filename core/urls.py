from django.conf.urls import url, include
from django.conf.urls import re_path
from rest_framework import routers
from django.conf.urls import re_path
from django.urls import path
from .views import *
from django.views.generic.base import TemplateView

from users.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

router = routers.DefaultRouter()
router.register('orders', OrderViewSet)
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('labels', LabelViewSet)
router.register('wishlist', WishListViewSet)
router.register('billing_address', BillingAddressViewSet)
router.register('transactions', TransactionViewSet)
# router.register('callback', Callback.as_view(), basename='callback')

urlpatterns = router.urls

urlpatterns = [
    path('callback/', callback, name="Callback"),
    path('redirect/', initiate_payment, name="payment"),

]
