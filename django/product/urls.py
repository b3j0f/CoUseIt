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

from django.conf.urls import url, include

from .views import (
    CategoryViewSet, ProductViewSet, SupplyViewSet, ConditionViewSet,
    StateViewSet, RequestViewSet, UsingViewSet, MediaViewSet, LocationViewSet,
    ProposalViewSet, GiveViewSet, ShareViewSet
)

from rest_framework import routers

router = routers.DefaultRouter()
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

urlpatterns = [
    url(r'', include(router.urls))
]
