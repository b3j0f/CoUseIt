"""View module."""

from .models import (
    Category, Product, State, Proposal, Location, Supply, Condition, Request,
    Using, Media
)
from .serializers import (
    CategorySerializer, ProductSerializer, StateSerializer, ProposalSerializer,
    MediaSerializer, UsingSerializer, RequestSerializer, ConditionSerializer,
    SupplySerializer, LocationSerializer
)
from .permissions import IsOwnerOrReadOnly, IsSupplierOrReadOnly

from rest_framework.viewsets import ModelViewSet


class LocationViewSet(ModelViewSet):
    """Location view set."""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_fields = {
        'id': ['exact'],
        'product': ['exact'],
        'longitude': ['exact', 'lte', 'gte'],
        'latitude': ['exact', 'lte', 'gte'],
        'datetime': ['exact', 'lte', 'gte'],
        'address': ['exact']
    }


class SupplyViewSet(ModelViewSet):
    """Supply view set."""

    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    filter_fields = {
        'id': ['exact'],
        'products': ['exact'],
        'vevent': ['exact']
    }


class ConditionViewSet(ModelViewSet):
    """Condition view set."""

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    filter_fields = {
        'id': ['exact'],
        'supply': ['exact'],
        'name': ['exact', 'iexact'],
        'quantity': ['exact', 'gte', 'lte'],
        'description': ['iexact']
    }


class RequestViewSet(ModelViewSet):
    """Request view set."""

    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_fields = {
        'id': ['exact'],
        'products': ['exact'],
        'accounts': ['exact'],
        'vevent': ['exact']
    }


class UsingViewSet(ModelViewSet):
    """Using view set."""

    queryset = Using.objects.all()
    serializer_class = UsingSerializer
    filter_fields = {
        'id': ['exact'],
        'accounts': ['exact'],
        'products': ['exact'],
        'request': ['exact'],
        'startts': ['exact', 'gte', 'lte'],
        'endts': ['exact', 'gte', 'lte']
    }


class MediaViewSet(ModelViewSet):
    """Media view set."""

    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_fields = {
        'id': ['exact'],
        'media': ['exact'],
        'product': ['exact'],
        'state': ['exact']
    }


class ProposalViewSet(ModelViewSet):
    """Proposal view set."""

    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filter_fields = {
        'id': ['exact'],
        'request': ['exact'],
        'condition': ['exact'],
        'quantity': ['exact', 'gte', 'lte'],
        'description': ['iexact']
    }


class CategoryViewSet(ModelViewSet):
    """Category view set."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = {
        'name': ['exact', 'iregex'],
        'parent': ['exact']
    }


class ProductViewSet(ModelViewSet):
    """Product view set."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = {
        'id': ['exact'],
        'name': ['exact', 'iregex'],
        'description': ['iregex'],
        'owners': ['exact'],
        'suppliers': ['exact'],
        'usings': ['exact'],
        'users': ['exact'],
        'categories': ['exact', 'iregex'],
        'stock': ['exact'],
        'conditions': ['exact'],
        'requests': ['exact'],
        'states': ['exact'],
        'locations': ['exact']
    }
    permission_classes = (IsOwnerOrReadOnly, IsSupplierOrReadOnly)


class StateViewSet(ModelViewSet):
    """State view set."""

    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_fields = {
        'name': ['exact'],
        'description': ['iregex']
    }
