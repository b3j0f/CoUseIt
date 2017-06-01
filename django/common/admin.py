"""Administration module."""

from django.contrib import admin

from .models import (
    Location, Product, Media, Supply, Condition, Request, State, Using,
    Category, VEvent, Stock, Service, Give, Share
)

# Register your models here.
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Service)
admin.site.register(Media)
admin.site.register(Supply)
admin.site.register(Condition)
admin.site.register(Request)
admin.site.register(State)
admin.site.register(Using)
admin.site.register(Category)
admin.site.register(VEvent)
admin.site.register(Give)
admin.site.register(Share)