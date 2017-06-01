"""Administration module."""

from django.contrib import admin

from .models import Account, Group, Message, MessageElement

# Register your models here.
admin.site.register(Account)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(MessageElement)
