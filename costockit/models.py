from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    parent = models.ForeignKey('Category', related_name='children')


class Stock(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)
    parent = models.ForeignKey('Stock', related_name='children')


class Product(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)
    suppliers = models.ManyToManyField(Account, related_name='supplies')
    categories = models.ForeignKey(Category)
    stock = models.ForeignKey(Stock)
