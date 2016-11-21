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
    CategoryViewSet, StockViewSet, ProductViewSet, CapacityViewSet,
    StatusViewSet, PlanningViewSet
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'products', ProductViewSet)
router.register(r'capacities', CapacityViewSet)
router.register(r'status', StatusViewSet)
router.register(r'plannings', PlanningViewSet)

urlpatterns = [url(r'rest/api/v1/', include(router.urls))]
