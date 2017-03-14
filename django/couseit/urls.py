"""simpleneed URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

from django.shortcuts import render

from rest_framework.routers import DefaultRouter

from .views import (
    homeview, aboutview, loginview, logoutview, resetpwdview,
    accountview, giveview, stockview, faqview, shareview, statsview
)

from account.views import UserViewSet, AccountViewSet
from product.views import (
    CategoryViewSet, ProductViewSet, SupplyViewSet, ConditionViewSet,
    StateViewSet, RequestViewSet, UsingViewSet, MediaViewSet, LocationViewSet,
    ProposalViewSet, GiveViewSet, ShareViewSet
)
from stock.views import StockViewSet, CapacityViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'states', StateViewSet)
router.register(r'conditions', ConditionViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'usings', UsingViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'supplyings', SupplyViewSet)
router.register(r'medias', MediaViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'gives', GiveViewSet)
router.register(r'shares', ShareViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'capatities', CapacityViewSet)

urlpatterns = [
    url(
        r'^{0}/auth/'.format(settings.API),
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^auth/', include('django.contrib.auth.urls'), name='auth'),
    url(r'^{0}/'.format(settings.API), include(router.urls), name='api'),
    url(r'^$', homeview),
    url(r'^home$', homeview),
    url(r'^faq', faqview),
    url(r'^about', aboutview),
    url(r'^login', loginview),
    url(r'^logout', logoutview),
    url(r'^resetpwd', resetpwdview),
    url(r'^account', accountview),
    url(r'^give', giveview),
    url(r'^share', shareview),
    url(r'^stock', stockview),
    url(r'^stats', statsview),
    url('test', lambda request: render(request, 'test.html'))
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
