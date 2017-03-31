"""View module."""

from product.views import ProductViewSet

from .models import Stock, Capacity, Container
from .serializers import (
    StockSerializer, CapacitySerializer, ContainerSerializer
)

from rest_framework.viewsets import ModelViewSet

from copy import deepcopy


class StockViewSet(ProductViewSet):
    """Stock view set."""

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_fields = deepcopy(ProductViewSet.filter_fields)
    filter_fields.update({
        'products': ['exact'],
        'capacities': ['exact'],
        'parent': ['exact']
    })


class CapacityViewSet(ModelViewSet):
    """Capacity view set."""

    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer
    filter_fields = {
        'categories': ['exact'],
        'amount': ['exact', 'lte', 'gte'],
        'stock': ['exact']
    }


class ContainerViewSet(ModelViewSet):
    """Container view set."""

    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    filter_fields = {
        'product': ['exact'],
        'stock': ['exact']
    }
