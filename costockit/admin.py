from django.contrib import admin

from .models import Account, Category, Stock, Product

# Register your models here.
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Product)
