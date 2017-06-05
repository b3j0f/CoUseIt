"""Account models."""
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from .utils import tostr


class Media(models.Model):
    """Media."""

    media = models.FileField(blank=True, default=None)
    url = models.CharField(max_length=255, blank=True, default=None)

    def furl(self):
        """Get final url."""
        return self.url if self.media is None else self.media.url


@python_2_unicode_compatible
class Account(models.Model):
    """CoUseIt account."""

    user = models.OneToOneField(User, primary_key=True)
    avatar = models.OneToOneField(Media, blank=True, default=None)
    relationships = models.ManyToManyField('self')
    lost_key = models.CharField(max_length=255)

    def __str__(self):
        """Representation."""
        return tostr(self, 'user.username')


@python_2_unicode_compatible
class Group(Account):
    """Account group."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(
        Account, blank=True, default=[], related_name='groups'
    )

    def __str__(self):
        """Representation."""
        return tostr(self, 'name')


@python_2_unicode_compatible
class ForbiddenEmail(models.Model):
    """Forbidden email."""

    email = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'email')


class MessageElement(models.Model):
    """Message element."""


@python_2_unicode_compatible
class Message(models.Model):
    """Account message."""

    author = models.ForeignKey(Account, blank=False, related_name='sent')
    title = models.CharField(max_length=256, blank=True, default=None)
    content = models.TextField(blank=False)
    created = models.DateTimeField()
    modified = models.DateTimeField(blank=True, default=None)
    to = models.ManyToManyField(Account, blank=True, related_name='inbox')
    element = models.ForeignKey(MessageElement, related_name='messages')
    replied_to = models.ForeignKey(
        'self', blank=True, related_name='responses'
    )
    read_at = models.DateTimeField(blank=True, default=None)

    class Meta:
        """Meta class."""

        default_related_name = 'messages'
        ordering = ['created']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        """Representation."""
        return tostr(
            self,
            'author', 'to', 'title', 'content', 'created', 'modified',
            'replied_to', 'read_at'
        )
