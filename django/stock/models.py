"""Stock models."""
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from product.models import Product, Category, tostr, Duration, Supply


@python_2_unicode_compatible
class Stock(Product):
    """Product stock model."""

    parent = models.ForeignKey(
        'self', blank=True, default=None, related_name='stocks'
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'address', 'parent')


@python_2_unicode_compatible
class Container(Duration):
    """Container product."""

    product = models.ForeignKey(Product, related_name='containers')
    amount = models.IntegerField(default=1, blank=True)
    stock = models.ForeignKey(Stock, related_name='products')
    supplyings = models.ManyToManyField(
        Supply, related_name='containers', blank=True, default=[]
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'amount', 'stock', 'supplyings ')


@python_2_unicode_compatible
class Capacity(models.Model):
    """Product stock capacity."""

    categories = models.ManyToManyField(
        Category, blank=True, related_name='capacities', default=[]
    )
    type = models.CharField(max_length=50, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False)
    stock = models.ForeignKey(Stock, blank=False, related_name='capacities')

    def __str__(self):
        """Representation."""
        return tostr(self, 'stock', 'categories.all', 'amount')
