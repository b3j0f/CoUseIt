"""Model module."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from address.models import AddressField

from account.models import Account, tostr

from time import time


@python_2_unicode_compatible
class Product(models.Model):
    """Product model."""

    name = models.CharField(max_length=50, blank=False)
    created = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    owners = models.ManyToManyField(
        Account, related_name='ownes', blank=False
    )
    suppliers = models.ManyToManyField(
        Account, related_name='supplies', blank=True
    )
    users = models.ManyToManyField(
        Account, related_name='uses', blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'id', 'name', 'categories')

    @property
    def location(self):
        """Last location."""
        return self.objects.order_by('-datetime').first()

    @property
    def using(self):
        """Last Using."""
        return self.usings.order_by('-datetime').first()

    @property
    def request(self):
        """Last request."""
        return self.requests.order_by('-datetime').first()


@python_2_unicode_compatible
class Supply(models.Model):
    """Product use condition."""

    products = models.ManyToManyField(
        Product, blank=False, related_name='supplies'
    )
    dates = models.ManyToManyField('VEvent')

    def __str__(self):
        """Representation."""
        return tostr(self, 'products', 'vevent')


class Share(Supply):
    """Share condition."""


class Give(Supply):
    """Give condition."""


@python_2_unicode_compatible
class Condition(models.Model):
    """Use condition item."""

    supply = models.ForeignKey(Supply, related_name='supplies')
    name = models.CharField(max_length=50)
    quantity = models.FloatField(default=1, blank=True)
    description = models.TextField(blank=True, default=None)

    def __str__(self):
        """Representation."""
        return tostr(self, 'supply', 'name', 'quantity', 'description')


@python_2_unicode_compatible
class Request(models.Model):
    """Request object."""

    products = models.ManyToManyField(
        Product, blank=False, related_name='requests'
    )
    accounts = models.ManyToManyField(Account, related_name='requests')
    vevent = models.CharField(max_length=255)

    def validate(self, request):
        """Check input request."""
        raise NotImplementedError()

    def __str__(self):
        """Representation."""
        return tostr(self, 'products', 'accounts', 'vevent')


@python_2_unicode_compatible
class Proposal(models.Model):
    """Proposal model."""

    request = models.ForeignKey(Request, related_name='proposals')
    condition = models.ForeignKey(Condition, related_name='proposals')
    quantity = models.FloatField(default=1, blank=True)
    description = models.TextField(blank=True, default=None)

    def __str__(self):
        """Representation."""
        return tostr(self, 'request', 'condition', 'quantity', 'description')


@python_2_unicode_compatible
class State(models.Model):
    """Product state."""

    detail = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField()
    product = models.ForeignKey(
        Product, related_name='states', null=True, blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'detail', 'medias', 'datetime')


@python_2_unicode_compatible
class Using(models.Model):
    """Using object."""

    accounts = models.ManyToManyField(
        Account, blank=False, related_name='usings'
    )
    products = models.ManyToManyField(
        Product, blank=False, related_name='usings'
    )
    request = models.OneToOneField(
        Request, blank=True, null=True, related_name='using'
    )
    startts = models.FloatField(default=time, blank=True)
    endts = models.FloatField(default=None, blank=True)

    def __str__(self):
        """Representation."""
        return tostr(
            self, 'accounts', 'products', 'request', 'startts', 'endts'
        )


class Media(models.Model):
    """Media."""

    media = models.FileField()
    product = models.ForeignKey(Product, related_name='medias')
    state = models.ForeignKey(State, related_name='medias')


@python_2_unicode_compatible
class Category(models.Model):
    """Product category model.

    A category has a unique name and has at most one parent category and can
    have several children category.
    """

    name = models.CharField(max_length=50, primary_key=True)
    parent = models.ForeignKey(
        'self', related_name='children', null=True, blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'parent', 'name')


@python_2_unicode_compatible
class Duration(models.Model):
    """Duration model."""

    startts = models.FloatField()
    endts = models.FloatField()

    def __str__(self):
        """Representation."""
        return tostr(self, 'endts', 'startts')


@python_2_unicode_compatible
class VEvent(models.Model):
    """VEvent model."""

    value = models.CharField(max_length=255)
    duration = models.IntegerField()
    periods = models.ManyToManyField(Duration, related_name='+', blank=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'value', 'duration', 'periods.all')


@python_2_unicode_compatible
class Location(Duration):
    """Product location."""

    product = models.ForeignKey(Product)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = AddressField()

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'address', 'latitude', 'longitude')
