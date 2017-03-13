"""Module urls."""

from django.conf.urls import url, include

from .views import UserViewSet, AccountViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
