from django.conf.urls import url, include
from rest_framework import routers
from users.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
