from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):

        return 'Account: {0}'.format(self.user)


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    parent = models.ForeignKey(
        'Category', related_name='children', default=None
    )

    def __str__(self):

        return 'Category: {0}/{0}'.format(self.parent, self.name)


class Stock(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)
    parent = models.ForeignKey('Stock', related_name='children', default=None)

    def __str__(self):

        return 'Stock: {0}/{1} ({2})'.format(self.parent, self.name, self.owner)


class Product(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)
    suppliers = models.ManyToManyField(Account, related_name='supplies')
    categories = models.ForeignKey(Category)
    stock = models.ForeignKey(Stock)

    def __str__(self):

        return 'Product: {0} {1}/{2} [{3}]'.format(
            self.name, self.stock, self.owner, self.categories
        )
