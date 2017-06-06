# coding: utf-8
"""Model module."""
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives


def sendemail(subject, msg, html, *to):
    """Send an email."""
    msg = EmailMultiAlternatives(subject, msg, '', to)
    msg.attach_alternative(html, "text/html")
    msg.send()


def getclientip(request):
    """Get client IP."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]

    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
