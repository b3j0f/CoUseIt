"""Serialization module."""

from .models import Stock, Capacity, Container

from product.serializers import ProductSerializer

from rest_framework.serializers import HyperlinkedModelSerializer


class StockSerializer(ProductSerializer):
    """Account serializer."""

    class Meta:
        """Account serializer meta class."""

        model = Stock
        fields = ProductSerializer.Meta.fields + ['parent']


class CapacitySerializer(HyperlinkedModelSerializer):
    """Capacity serializer."""

    class Meta:
        """Capacity serializer meta class."""

        model = Capacity
        fields = ['stock', 'categories', 'amount']


class ContainerSerializer(HyperlinkedModelSerializer):
    """Container serializer."""

    class Meta:
        """Container serializer meta class."""

        model = Container
        fields = ['product', 'stock']
