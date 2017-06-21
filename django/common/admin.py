"""Administration module."""

from django.contrib import admin

from .models import (
    Location, Product, Media, Supplying, Condition, Request, State, Using,
    Category, VEvent, Stock, Service, Giving, Sharing, Stocking, Providing,
    Property, PropertyType
)

# Register your models here.
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Service)
admin.site.register(Media)
admin.site.register(Supplying)
admin.site.register(Condition)
admin.site.register(Request)
admin.site.register(State)
admin.site.register(Using)
admin.site.register(Category)
admin.site.register(VEvent)
admin.site.register(Giving)
admin.site.register(Sharing)
admin.site.register(Stocking)
admin.site.register(Providing)
admin.site.register(Property)
admin.site.register(PropertyType)
