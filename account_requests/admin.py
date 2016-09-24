from django.contrib import admin

from .models import CRUD, StateRequest, AccountRequest

# Register your models here.
admin.site.register(CRUD)
admin.site.register(StateRequest)
admin.site.register(AccountRequest)
