# coding: utf-8
"""Model module."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver
from django.conf import settings

from address.models import AddressField

from account.models import Account, MessageElement, tostr, Media

from time import time

from datetime import date

from collections import namedtuple

PropertyProps = namedtuple('PropertyProps', ('name', 'unit', 'values'))


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
        Category, related_name='commons', blank=False, null=False,
        db_index=True
    )
    professional = models.BooleanField(db_index=True, blank=True, default=True)
    medias = models.ManyToManyField(
        Media, blank=True, default=[], related_name='+'
    )

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

    @property
    def _self(self):
        """Get child reference."""
        result = self
        for attr in ('_stock', '_service', '_package', '_product'):
            try:
                result = getattr(self, attr)

            except AttributeError:
                continue

            else:
                break

        return result


class Product(Common):
    """Product model."""

    base = models.OneToOneField(
        Common, parent_link=True, related_name='_product', blank=True
    )

    quantity = models.IntegerField(default=1, blank=True)

    tostock = models.BooleanField(default=False, blank=True, db_index=True)
    stock = models.ForeignKey('Stock', blank=True, default=None)


class Stock(Product):
    """Product stock model."""

    _base = models.OneToOneField(
        Product, parent_link=True, related_name='_stock', blank=True
    )

    capacity = models.IntegerField(default=1, blank=True)
    contentcategory = models.ForeignKey(
        Category, blank=True, null=False, db_index=True
    )


class Service(Common):
    """Service model."""

    base = models.OneToOneField(
        Common, parent_link=True, related_name='_service', blank=True
    )


class Package(Product):
    """Package of commons."""

    _base = models.OneToOneField(
        Product, parent_link=True, related_name='_package', blank=True
    )

    commons = models.ManyToManyField(Common)


@python_2_unicode_compatible
class Supplying(MessageElement):
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
    maxusers = models.IntegerField(default=float('inf'), blank=True)
    bid = models.BooleanField(default=True, blank=True)

    sharedwith = models.ManyToManyField(Account, blank=True, default=[])
    public = models.BooleanField(default=True, blank=True)
    enable = models.BooleanField(default=True, blank=True)

    suppliers = models.ManyToManyField(
        Account, related_name='supplyings', blank=True
    )

    class Meta:
        """Meta class."""

        default_related_name = 'supplyings'
        get_latest_by = 'dates'
        order_with_respect_to = 'common'
        verbose_name = 'supplying'
        verbose_name_plural = 'supplyings'

    def __str__(self):
        """Representation."""
        return tostr(self, 'common', 'name', 'description', 'amount')

    @property
    def objective(self):
        """Get objective."""
        result = {}

        for cond in self.conditions:
            if cond.currency.name in result:
                result[cond.currency.name] += cond.amount

            else:
                result[cond.currency.name] = cond.amount

        return result


class Giving(Supplying):
    """Giving model."""


class Providing(Supplying):
    """Providing model."""


class Sharing(Supplying):
    """Sharing model."""

    minduration = models.IntegerField(null=True, default=None, blank=True)
    maxduration = models.IntegerField(null=True, default=None, blank=True)

    period = models.CharField(
        default=None, max_length=50, null=True,
        choices=(
            ('u', 'unlimited'),
            ('h', 'hours'),
            ('d', 'days'),
            ('w', 'weeks'),
            ('e', 'weekends'),
            ('m', 'months'),
            ('y', 'years')
        )
    )


class Stocking(Supplying):
    """Stocking model."""


@python_2_unicode_compatible
class Currency(models.Model):
    """Currency model."""

    name = models.CharField(max_length=50)

    def __str__(self):
        """Representation."""
        return self.name


@python_2_unicode_compatible
class Condition(models.Model):
    """Supplying condition item."""

    class Meta:
        """Meta class."""

        default_related_name = 'conditions'
        verbose_name = 'condition'
        order_with_respect_to = 'supplying'
        verbose_name_plural = 'conditions'

    currency = models.ForeignKey(Currency, blank=True, default=None)
    amount = models.FloatField(default=1, blank=True)
    description = models.TextField(blank=True, default=None, null=True)
    supplying = models.ForeignKey(
        Supplying, related_name='conditions', null=True
    )
    maxbid = models.FloatField(default=None, null=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'supplying', 'amount', 'currency', 'maxbid')


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

    common_amount = models.IntegerField(default=1, blank=True)

    # 4 choices of supplyments

    # specific common
    supplyment = models.ForeignKey(
        Supplying, blank=True, default=None, related_name='requests'
    )
    # money/metric quantity
    currency = models.ForeignKey(Currency, blank=True, default=None)
    amount = models.FloatField(default=None, blank=True)
    # description common type
    description = models.CharField(blank=True, default=None, max_length=255)
    # category common type
    category = models.ForeignKey(
        Category, blank=True, default=None, related_name='requests'
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

    @property
    def objective(self):
        """Objective."""
        result = None

        if self.supplyment:
            result = self.supplyment.objective

        else:
            result = {self.currency.name: self.amount}

        if self.common_amount > 1:
            for key in result:
                result[key] *= self.common_amount

        return result

    @property
    def current_amount(self):
        """Current amount."""
        result = {}

        for proposal in self.proposals:
            for cond in proposal.condition:
                key = cond.currency if cond.currency else cond.metric
                if key in result:
                    result[key] += proposal.amount
                else:
                    result[key] = proposal.amount

        return result

    @property
    def succeedpct(self):
        """Get succeed pct."""
        objective = self.objective
        total = sum(objective.keys())

        current_amount = self.current_amount

        diff = 0

        for key in objective:
            objamount = objective[key]
            if key in current_amount:
                diff += min(objamount, current_amount[key])

        return diff * 100 / total


@python_2_unicode_compatible
class Proposal(models.Model):
    """Proposal model."""

    request = models.ForeignKey(Request, related_name='proposals')
    condition = models.ForeignKey(Condition, related_name='proposals')
    amount = models.FloatField(default=1, blank=True)
    description = models.TextField(blank=True, default=None)

    def __str__(self):
        """Representation."""
        return tostr(self, 'request', 'condition', 'amount', 'description')


@python_2_unicode_compatible
class State(models.Model):
    """Product state."""

    detail = models.TextField(null=True, blank=True, default=None)
    datetime = models.DateTimeField()
    product = models.ForeignKey(
        Product, related_name='states', null=True, blank=True, default=None
    )
    medias = models.ManyToManyField(
        Media, blank=True, default=[], related_name='+'
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
class PropertyType(models.Model):
    """Property type model."""

    name = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    attrs = models.ManyToManyField('self', blank=True, default=[])
    categories = models.ManyToManyField(
        Category, related_name='properties', blank=True
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name', 'type', 'categories', 'unit', 'values')

    @property
    def _self(self):
        """Child instance."""
        result = self

        for field in []:
            result = getattr(self, field)
            if result is not None:
                break

        return result

    @property
    def attrvalues(self):
        """Get attr values."""
        result = {}

        values = self.values.split('|')

        for attr in self.attrs:
            result[attr.name] = values.pop(0)

        return result

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

    @property
    def display_name(self):
        """Return display name."""
        return self.name.replace('_', ' ')


@python_2_unicode_compatible
class Property(models.Model):
    """Common property."""

    common = models.ForeignKey(Common, related_name='properties')
    type = models.ForeignKey(PropertyType, related_name='properties')
    value = models.CharField(max_length=50, blank=True, default=None)

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
