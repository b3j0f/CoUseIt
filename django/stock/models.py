"""Stock models."""
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from product.models import (
    Product, Category, tostr, Duration, Supply, ConditionSet
)


@python_2_unicode_compatible
class Stock(Product):
    """Product stock model."""

    parent = models.ForeignKey(
        'self', blank=True, default=None, related_name='stocks'
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'address', 'parent')


class Stocking(Supply):
    """Stocking model."""

    stock = models.ForeignKey(Stock, related_name='conditions')
    conditions = models.ManyToManyField(ConditionSet, related_name='+')

    class Meta:
        """Meta class."""

        default_related_name = 'stockings'
        order_with_respect_to = 'stock'
        verbose_name = 'stocking'
        verbose_name_plural = 'stockings'


class Container(Duration):
    """Container product."""

    product = models.ForeignKey(Product, related_name='containers')
    stock = models.ForeignKey(Stock, related_name='products')

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'stock')


@python_2_unicode_compatible
class Capacity(models.Model):
    """Product stock capacity."""

    categories = models.ManyToManyField(
        Category, blank=False, related_name='capacities'
    )
    amount = models.FloatField(blank=False, null=False)
    stock = models.OneToOneField(Stock, blank=False, related_name='capacities')

    def __str__(self):
        """Representation."""
        return tostr(self, 'stock', 'categories.all', 'amount')
