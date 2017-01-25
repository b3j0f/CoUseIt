"""Account models."""
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from .utils import tostr


@python_2_unicode_compatible
class Account(models.Model):
    """CoUseIt account."""

    user = models.OneToOneField(User, primary_key=True)
    avatar = models.FileField()
    relationships = models.ManyToManyField('self')
    lost_key = models.CharField(max_length=255)

    def __str__(self):
        """Representation."""
        return tostr(self, 'user.username')


@python_2_unicode_compatible
class ForbiddenEmail(models.Model):
    """Forbidden email."""

    email = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'email')
