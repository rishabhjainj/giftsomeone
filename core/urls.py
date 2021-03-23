from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from users.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

router = routers.DefaultRouter()
router.register('products/all', ProductViewSet)
router.register('orders/all', OrderViewSet)
router.register('categories', CategoryViewSet)
router.register('labels', LabelViewSet)

