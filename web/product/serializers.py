"""Serialization module."""

from .models import (
    Product, Location, Media, Supply, Condition, Request, State, Using,
    Category, Proposal, Share, Give, VEvent, Duration
)

from rest_framework.serializers import HyperlinkedModelSerializer

from .permissions import (
    IsOwnerOrReadOnly, IsSupplierOrReadOnly, IsUserOrReadOnly
)


class ProposalSerializer(HyperlinkedModelSerializer):
    """Proposal serializer."""

    permission_classes = (
        IsOwnerOrReadOnly, IsSupplierOrReadOnly, IsUserOrReadOnly,
    )

    class Meta:
        """Proposal serializer meta class."""

        model = Proposal
        fields = ['id', 'request', 'condition', 'quantity', 'description']


class ProductSerializer(HyperlinkedModelSerializer):
    """Product serializer."""

    permission_classes = (IsOwnerOrReadOnly,)

    class Meta:
        """Product serializer meta class."""

        model = Product
        fields = [
            'id', 'name', 'description',
            'owners', 'suppliers', 'users', 'usings', 'categories',
            'states', 'supplies', 'requests', 'locations'
        ]


class LocationSerializer(HyperlinkedModelSerializer):
    """Location serializer."""

    class Meta:
        """Location serializer meta class."""

        model = Location
        fields = ['product', 'longitude', 'latitude', 'datetime', 'address']


class MediaSerializer(HyperlinkedModelSerializer):
    """Media serializer."""

    class Meta:
        """Media serializer meta class."""

        model = Media
        fields = ['product', 'media', 'state']


class SupplySerializer(HyperlinkedModelSerializer):
    """Supply serializer."""

    permission_classes = (IsSupplierOrReadOnly,)

    class Meta:
        """Supply serializer meta class."""

        model = Supply
        fields = ['products', 'vevent']


class ConditionSerializer(HyperlinkedModelSerializer):
    """Condition serializer."""

    permission_classes = (IsSupplierOrReadOnly,)

    class Meta:
        """Condition serializer meta class."""

        model = Condition
        fields = ['supply', 'name', 'quantity', 'description']


class RequestSerializer(HyperlinkedModelSerializer):
    """Request serializer."""

    permission_classes = (IsUserOrReadOnly,)

    class Meta:
        """Request serializer meta class."""

        model = Request
        fields = ['products', 'accounts', 'vevent']


class StateSerializer(HyperlinkedModelSerializer):
    """State serializer."""

    class Meta:
        """State serializer meta class."""

        model = State
        fields = ['detail', 'medias', 'datetime']


class UsingSerializer(HyperlinkedModelSerializer):
    """Using serializer."""

    permission_classes = (IsUserOrReadOnly,)

    class Meta:
        """Using serializer meta class."""

        model = Using
        fields = ['accounts', 'products', 'request', 'startts', 'endts']


class CategorySerializer(HyperlinkedModelSerializer):
    """Category serializer."""

    class Meta:
        """Category serializer meta class."""

        model = Category
        fields = ['name', 'parent', 'children']


class ShareSerializer(SupplySerializer):
    """Share serializer."""

    class Meta:
        """Share serializer meta class."""

        model = Share
        fields = list(SupplySerializer.Meta.fields)


class GiveSerializer(SupplySerializer):
    """Give serializer."""

    class Meta:
        """Give serializer meta class."""

        model = Give
        fields = list(SupplySerializer.Meta.fields)


class DurationSerializer(HyperlinkedModelSerializer):
    """Duration serializer."""

    class Meta:
        """Duration serializer meta class."""

        model = Duration
        fields = ['endts', 'startts']


class VEventSerializer(DurationSerializer):
    """VEvent serializer."""

    class Meta:
        """VEvent serializer meta class."""

        model = VEvent
        fields = ['value', 'duration'] + list(DurationSerializer.Meta.fields)
