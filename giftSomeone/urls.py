"""giftSomeone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from core.urls import router as core_router
from users.urls import router as user_router

from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


router = DefaultRouter()
router.registry.extend(core_router.registry)
router.registry.extend(user_router.registry)
urlpatterns = [
    path(r'admin/', admin.site.urls),
    re_path(r'api/', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    #include function allows referencing other URLConfs
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
