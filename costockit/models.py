from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Stock(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)


class Product(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Account)
    suppliers = models.ManyToManyField(Account, related_name='supplies')
    categories = models.ForeignKey(Category)
    stock = models.ForeignKey(Stock)
