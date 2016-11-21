"""View module."""

from .models import Category, Stock, Product, Capacity, Status, Planning
from .serializers import (
    CategorySerializer, StockSerializer, ProductSerializer, CapacitySerializer,
    StatusSerializer, PlanningSerializer, ConditionSerializer
)
from .permissions import IsOwnerOrReadOnly

from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = {
        'id': ['exact', 'iregex'],
        'name': ['exact', 'iregex'],
        'parent': ['exact']
    }


class StockViewSet(ModelViewSet):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'iregex'],
        'description': ['iregex'],
        'owners': ['exact'],
        'suppliers': ['exact'],
        'latitude': ['exact', 'gte', 'lte'],
        'longitude': ['exact', 'gte', 'lte'],
        'address': ['exact'],
        'parent': ['exact']
    }
    permission_classes = (IsOwnerOrReadOnly)


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'iregex'],
        'description': ['iregex'],
        'owners': ['exact'],
        'suppliers': ['exact'],
        'users': ['exact'],
        'categories': ['exact'],
        'stock': ['exact']
    }
    permission_classes = (IsOwnerOrReadOnly)


class CapacityViewSet(ModelViewSet):

    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer
    filter_fields = {
        'categories': ['exact'],
        'amount': ['exact', 'lte', 'gte']
    }


class StatusViewSet(ModelViewSet):

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_fields = {
        'name': ['exact'],
        'description': ['iregex']
    }


class PlanningViewSet(ModelViewSet):

    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer
    filter_fields = {
        'id': ['exact'],
        'products': ['exact'],
        'calendar': ['exact', 'iregex'],
        'conditions': ['exact'],
        'status': ['exact'],
        'user': ['exact'],
        'source': ['exact'],
        'target': ['exact']
    }
