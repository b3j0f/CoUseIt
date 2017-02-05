"""Model module."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver

from address.models import AddressField

from account.models import Account, tostr

from time import time
from datetime import date


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
    category = models.ForeignKey(
        'Category', related_name='products', blank=False, null=False
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'id', 'name', 'category')

    @property
    def location(self):
        """Last location."""
        return self.locations.order_by('-datetime').first()

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

    dates = models.ManyToManyField('VEvent')
    endts = models.FloatField(null=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'products', 'vevent')


class Share(Supply):
    """Share condition."""

    products = models.ForeignKey(Product, related_name='shares')


class Give(Supply):
    """Give condition."""

    products = models.ForeignKey(Product, related_name='gives')


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
class Enjoynment(models.Model):
    """Enjoyment model."""

    value = models.IntegerField()

    def __str__(self):
        """Representation."""
        return tostr(self, 'value')


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
class ParentCategory(models.Model):
    """Product parent category model.

    A parent category has a unique name.
    """

    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        """Representation."""
        return tostr(self, 'name')


@python_2_unicode_compatible
class Category(models.Model):
    """Product category model.

    A category has a unique name and a parent category.
    """

    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)
    parent = models.ForeignKey(ParentCategory, related_name='categories')

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'parent')

    @property
    def allproperties(self):
        """Get all properties from this parent category and this.

        rtype: list
        """
        return list(self.parent.properties.all()) + list(self.properties.all())


@python_2_unicode_compatible
class TypeProperty(models.Model):
    """Type Property model."""

    name = models.CharField(max_length=50, primary_key=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    parentcategories = models.ManyToManyField(
        ParentCategory, related_name='properties', blank=True
    )
    categories = models.ManyToManyField(
        Category, related_name='properties', blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'categories', 'unit', 'values', 'depends')

    @property
    def allvalues(self):
        """Get an array of values.

        Values are strings separated by:
        - '|'
        - '-' which designates a range of integer values.

        :rtype: list
        """
        result = None

        if self.values is not None:
            result = self.values.split('|')

            if len(result) == 1:
                result = result[0].split('-')

                minval = result[0]
                maxval = result[1]

                minplus = '+' in minval
                maxplus = '+' in maxval

                result = [
                    str(val) for val in range(int(minval), int(maxval) + 1)
                ]

                if minplus:
                    result[0] = minval

                if maxplus:
                    result[-1] = maxval

        return result


@python_2_unicode_compatible
class Property(models.Model):
    """Product property."""

    product = models.ForeignKey(Product, related_name='properties')
    type = models.ForeignKey(TypeProperty, related_name='properties')
    value = models.CharField(max_length=50)

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'type', 'value')


@python_2_unicode_compatible
class CustomProperty(Property):
    """Custom property."""

    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'type', 'value', 'unit', 'description')


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

    product = models.OneToOneField(Product)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = AddressField()

    def __str__(self):
        """Representation."""
        return tostr(self, 'product', 'address', 'latitude', 'longitude')


@python_2_unicode_compatible
class Stat(models.Model):
    """Statistic model."""

    date = models.DateField(default=date.today)
    owners = models.IntegerField()
    suppliers = models.IntegerField()
    users = models.IntegerField()
    usingduration = models.FloatField()

    def __str__(self):
        """Representation."""
        return tostr(
            self, 'date', 'owners', 'suppliers', 'users', 'usingduration'
        )


@python_2_unicode_compatible
class Status(models.Model):
    """Status modle."""

    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'description')


def getorcreatestat(**kwargs):
    """Get or create a stat with input field and value."""
    result, created = Stat.get_or_create(
        date=date.today(), default=kwargs
    )

    if not created:
        for field in list(kwargs):
            kwargs[field] = F(field) + kwargs[field]
        Stat.objects.filter(id=result.id).update(**kwargs)

    return result


@receiver(post_save, sender=Using)
def statusing(sender, instance, **kwargs):
    """Save duration in stats."""
    if instance.endts is not None:
        elapsedtime = instance.endts - instance.startts
        getorcreatestat(usingduration=elapsedtime)
