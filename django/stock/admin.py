"""Administration module."""

from django.contrib import admin

from .models import Stock, Capacity, Container

# Register your models here.
admin.site.register(Stock)
admin.site.register(Capacity)
admin.site.register(Container)
