"""Model module."""

from django.db import models
from django.contrib.auth.models import User
from address.models import AddressField


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
        return 'Category: {0}/{0}'.format(self.parent.name, self.name)


class Stock(models.Model):
    """Product stock model.

    properties:

    - contain products.
    - is owned by at least one user.
    - is accessible from at least one supplier with less access rights than
        owners.
    - has a location or an address.
    """

    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    owners = models.ManyToManyField(User, blank=False)
    suppliers = models.ManyToManyField(
        User, blank=True, related_name='manages'
    )

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    address = AddressField(blank=True, null=True)

    parent = models.ForeignKey(
        'self', related_name='children', null=True, blank=True
    )

    def __str__(self):
        """Representation."""
        return 'Stock: {0}/{1} ({2})'.format(
            self.parent.name, self.name, self.owners, self.address
        )


class Product(models.Model):
    """Product model."""

    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True, null=True)
    owners = models.ManyToManyField(User, blank=False)
    suppliers = models.ManyToManyField(
        User, related_name='supplies', blank=True
    )
    users = models.ManyToManyField(User, blank=True, related_name='uses')
    categories = models.ManyToManyField(Category, blank=False)
    stock = models.ForeignKey(Stock, blank=True, null=True)

    def __str__(self):
        """Representation."""
        return 'Product: {0} {1}/{2} [{3}]'.format(
            self.id, self.name, self.stock, self.owners, self.categories.all()
        )


class Capacity(models.Model):
    """Product stock capacity."""

    categories = models.ManyToManyField(Category, blank=False)
    amount = models.FloatField(blank=False, null=False)

    def __str__(self):
        """Representation."""
        return 'Category: {0} ({1})'.format(self.categories.all(), self.amount)


class Status(models.Model):
    """Planning state."""

    name = models.CharField(max_length=30, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representation."""
        return 'State: {0}/{1}'.format(self.name, self.description)


class Planning(models.Model):
    """Product planning."""

    products = models.ManyToManyField(Product, blank=False)
    calendar = models.TextField(blank=False, null=False)
    conditions = models.ManyToManyField('Condition', blank=True)
    status = models.ForeignKey(Status, default='PENDING', blank=True)
    user = models.ManyToManyField(User, blank=False)
    source = models.ForeignKey(
        Stock, blank=False, null=False, related_name='+'
    )
    target = models.ForeignKey(Stock, blank=True, null=True, related_name='+')

    def validate(self):
        """Validate all input conditions."""
        for condition in self.conditions.all():
            condition.validate(self)


class Condition(models.Model):
    """Condition planning use."""

    def validate(self, planning):
        """Check input planning."""
        raise NotImplementedError()
