from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from users.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

router = routers.DefaultRouter()
router.register('orders', OrderViewSet)
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('labels', LabelViewSet)
router.register('wishlist', WishListViewSet)

urlpatterns = router.urls
# urlpatterns += [
#     url(r'^orders/$', OrderViewSet, name='order_list'),
# ]
