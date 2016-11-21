"""Administration module."""

from django.contrib import admin

from .models import Category, Stock, Product, Capacity, Planning, Condition

# Register your models here.
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(Capacity)
admin.site.register(Planning)
admin.site.register(Condition)
