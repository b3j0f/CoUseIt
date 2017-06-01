# coding: utf-8
"""Model module."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.conf import settings

from address.models import AddressField

from account.models import Account, MessageElement, tostr

from time import time

from datetime import date

from collections import namedtuple


@python_2_unicode_compatible
class Common(MessageElement):
    """Common model."""

    class Meta:
        """Meta class."""

        default_related_name = 'commons'
        get_latest_by = 'created'
        ordering = ['created']
        unique_together = ()
        index_together = []
        verbose_name = 'common'
        verbose_name_plural = 'commons'

    name = models.CharField(db_index=True, max_length=50, blank=False)
    created = models.DateTimeField(blank=True)
    shortdescription = models.CharField(
        blank=True, null=True, max_length=120
    )
    description = models.CharField(blank=True, null=True, max_length=255)
    owners = models.ManyToManyField(
        Account, related_name='ownes', blank=False
    )
    suppliers = models.ManyToManyField(
        Account, related_name='supplyings', blank=True
    )
    users = models.ManyToManyField(
        Account, related_name='uses', blank=True
    )
    category = models.ForeignKey(
        'Category', related_name='commons', blank=False, null=False,
        db_index=True
    )
    professional = models.BooleanField(db_index=True, blank=True, default=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'id', 'name', 'category', 'professional', 'amount')

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


class Product(Common):
    """Product model."""

    amount = models.IntegerField(default=1, blank=True)

    tostock = models.BooleanField(default=False, blank=True, db_index=True)


class Stock(Product):
    """Product stock model."""

    parent = models.ForeignKey(
        'self', blank=True, default=None, related_name='stocks'
    )
    pamount = models.IntegerField(default=1, blank=True)
    pcategory = models.ForeignKey(
        'Category', blank=True, null=False, db_index=True
    )


class Service(Common):
    """Service model."""


@python_2_unicode_compatible
class Supply(MessageElement):
    """Common use condition."""

    common = models.ForeignKey(Common, related_name='supplyings')
    name = models.CharField(max_length=50, blank=True, default=None, null=True)
    description = models.CharField(
        max_length=255, blank=True, default=None, null=True
    )
    dates = models.ManyToManyField('VEvent', related_name='+')
    amount = models.IntegerField(default=1, blank=True)
    startdate = models.DateTimeField(default=None, blank=True, null=True)
    duedate = models.DateTimeField(default=None, blank=True, null=True)

    peruser = models.BooleanField(default=False, blank=True)
    minusers = models.IntegerField(default=1, blank=True)
    maxusers = models.IntegerField(default=None, null=True, blank=True)
    bid = models.BooleanField(default=False, blank=True)
    minduration = models.IntegerField(null=True, default=None, blank=True)
    maxduration = models.IntegerField(null=True, default=None, blank=True)

    class Meta:
        """Meta class."""

        default_related_name = 'supplyings'
        get_latest_by = 'dates'
        order_with_respect_to = 'common'
        verbose_name = 'supply'
        verbose_name_plural = 'supplyings'

    def __str__(self):
        """Representation."""
        return tostr(self, 'common', 'name', 'description', 'amount')


class Give(Supply):
    """Give model."""


class Share(Supply):
    """Share model."""

    period = models.CharField(
        default=None, max_length=50, null=True,
        choices=(
            ('u', 'unlimited'),
            ('d', 'days'),
            ('w', 'weeks'),
            ('e', 'weekends'),
            ('m', 'months'),
            ('y', 'years')
        )
    )


@python_2_unicode_compatible
class Condition(models.Model):
    """Use condition item."""

    class Meta:
        """Meta class."""

        default_related_name = 'conditions'
        verbose_name = 'condition'
        order_with_respect_to = 'supply'
        verbose_name_plural = 'conditions'

    type = models.CharField(max_length=50)
    amount = models.FloatField(default=1, blank=True)
    description = models.TextField(blank=True, default=None, null=True)
    supply = models.ForeignKey(Supply, related_name='conditions', null=True)
    maxbid = models.ForeignKey(
        Supply, related_name='maxbidconditions', null=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'type', 'amount', 'description', 'supply')


@python_2_unicode_compatible
class Request(MessageElement):
    """Request object."""

    class Meta:
        """Meta class."""

        default_related_name = 'requests'
        get_latest_by = 'created'
        ordering = ['created']
        verbose_name = 'request'
        verbose_name_plural = 'requests'

    created = models.DateTimeField()  # created by an account
    # accepted by a common supplyer
    accepted = models.DateTimeField(blank=True, null=True)
    # cancelation a common supplyer
    canceled = models.DateTimeField(blank=True, null=True)
    # supplyer who has accepted/canceled to the request
    supplyer = models.ForeignKey(
        Account, blank=True, null=True, related_name='answers'
    )
    amount = models.IntegerField(default=1, blank=True)
    supplyment = models.ForeignKey(
        Supply, blank=False, null=False, related_name='requests'
    )
    accounts = models.ManyToManyField(Account, related_name='requests')
    frominterval = models.DateTimeField(blank=True, null=True)
    tointerval = models.DateTimeField(blank=True, null=True)
    public = models.BooleanField(default=True, null=False)

    @property
    def answered(self):
        """Get datetime supplyer answer."""
        return self.accepted or self.canceled

    def validate(self, request):
        """Check input request."""
        raise NotImplementedError()

    def __str__(self):
        """Representation."""
        return tostr(self, 'accounts', '')


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

    detail = models.TextField(null=True, blank=True, default=None)
    datetime = models.DateTimeField()
    product = models.ForeignKey(
        Product, related_name='states', null=True, blank=True, default=None
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
    commons = models.ManyToManyField(
        Common, blank=False, related_name='usings'
    )
    request = models.OneToOneField(
        Request, blank=True, null=True, related_name='using'
    )
    startts = models.FloatField(default=time, blank=True)
    endts = models.FloatField(default=None, blank=True)

    def __str__(self):
        """Representation."""
        return tostr(
            self, 'accounts', 'commons', 'request', 'startts', 'endts'
        )


@python_2_unicode_compatible
class Enjoynment(models.Model):
    """Enjoyment model."""

    value = models.IntegerField()
    account = models.ForeignKey(Account)
    request = models.ForeignKey(Request, blank=True, default=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'account', 'request', 'value')


class Media(models.Model):
    """Media."""

    media = models.FileField()
    common = models.ForeignKey(Common, related_name='medias')
    state = models.ForeignKey(State, related_name='medias')


@python_2_unicode_compatible
class Category(models.Model):
    """Common category model.

    Unique name per parent.

    Only categories without children can be associated to a common.
    """

    class Meta:
        """Meta class."""

        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(
        max_length=255, blank=True, default=None, null=True
    )
    types = models.CharField(max_length=50)
    media = models.ForeignKey(
        Media, blank=True, null=True, default=None, related_name='+'
    )
    parent = models.ForeignKey(
        'self', related_name='children', blank=True, default=None, null=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'description')

    @property
    def allproperties(self):
        """Get all properties from this parent category and this.

        rtype: list
        """
        result = list(self.properties.all())

        if self.parent is not None:
            result = self.parent.allproperties + result

        return result

    @property
    def allpropertieswvalues(self):
        """Get all property values."""
        result = []

        for prop in self.allproperties:

            if prop.values is None:
                properties = prop.properties.filter(common__category=self)

                if settings.DEBUG:
                    values = sorted(set(prop.value for prop in properties))

                else:
                    values = list(
                        properties.order_by('value').distinct('value')
                    )

            else:
                values = prop.allvalues

            result.append(PropertyProps(prop.name, prop.unit, values))

        return result

    @property
    def display_name(self):
        """Get display name."""
        return self.name.replace('_', ' ')


PropertyProps = namedtuple('PropertyProps', ('name', 'unit', 'values'))


@python_2_unicode_compatible
class TypeProperty(models.Model):
    """Type Property model."""

    name = models.CharField(max_length=50, primary_key=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(
        Category, related_name='properties', blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'categories', 'unit', 'values')

    @property
    def allvalues(self):
        """Get an array of values.

        Values are strings separated by:
        - '|'
        - '-' which designates a range of integer values.

        :rtype: list
        """
        result = []

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
    """Common property."""

    common = models.ForeignKey(Common, related_name='properties')
    type = models.ForeignKey(TypeProperty, related_name='properties')
    value = models.CharField(max_length=50)

    def __str__(self):
        """Representation."""
        return tostr(self, 'common', 'type', 'value')


@python_2_unicode_compatible
class CustomProperty(Property):
    """Custom property."""

    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'common', 'type', 'value', 'unit', 'description')


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

    common = models.ForeignKey(Common, related_name='locations')
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = AddressField()

    def __str__(self):
        """Representation."""
        return tostr(self, 'address', 'latitude', 'longitude')


@python_2_unicode_compatible
class Stat(models.Model):
    """Statistical model."""

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
    """Status model."""

    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'description')


@python_2_unicode_compatible
class WordsByCommon(models.Model):
    """Words with commons."""

    word = models.CharField(max_length=255, primary_key=True)
    commons = models.ManyToManyField(Common, related_name='+')

    def __str__(self):
        """Representation."""
        return self.word


@receiver(post_save, sender=Common)
def updatewords(sender, instance, **kwargs):
    """Update words by common name and description."""
    wnames = instance.name.split(' ')
    wdescription = instance.description.split(' ')
    wcats = [cat.name for cat in instance.categories.all()]
    wprops = [prop.name for prop in instance.properties.all()]

    for word in wnames + wdescription + wcats + wprops:
        WordsByCommon.get_or_create(word=word).commons.add(instance).save()


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
