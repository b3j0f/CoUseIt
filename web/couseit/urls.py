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

from .views import (
    homeview, aboutview, loginview, logoutview, resetpwdview,
    accountview, giveview, stockview, faqview, shareview, statsview
)

urlpatterns = [
    url(
        r'^api/v1/auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^auth/', include('django.contrib.auth.urls'), name='auth'),
    url(r'^api/v1/', include('account.urls'), name='account'),
    url(r'^api/v1/', include('product.urls'), name='product'),
    url(r'^api/v1/', include('stock.urls'), name='stock'),
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
    url(r'^stats', statsview)
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
