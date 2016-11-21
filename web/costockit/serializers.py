"""Serialization module."""

from .models import (
    Category, Stock, Product, Capacity, Status, Planning, Condition
)

from rest_framework.serializers import HyperlinkedModelSerializer


class CategorySerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Category
        fields = ['name', 'parent', 'children']


class StockSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Stock
        fields = [
            'id', 'name', 'description', 'owners', 'suppliers',
            'latitude', 'longitude', 'address',
            'parent', 'children'
        ]


class ProductSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Product
        fields = [
            'id', 'name', 'description',
            'owners', 'suppliers', 'users', 'categories', 'stock'
        ]


class CapacitySerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Capacity
        fields = ['categories', 'amount']


class StatusSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Status
        fields = ['name', 'description']


class PlanningSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Planning
        fields = [
            'id', 'products', 'calentar', 'conditions', 'status',
            'user', 'source', 'target'
        ]


class ConditionSerializer(HyperlinkedModelSerializer):

    class Meta:

        model = Condition
        fields = ['']
